#!/usr/bin/env python3
"""Fail the build when the reveal animation is half-wired.

Written because it already broke, on all eight pages at once, in the pass that
introduced it. The insert script guarded with `if "flow.js" not in page` — and
the <head> snippet's own comment names /assets/js/flow.js. So the guard matched
a comment, concluded the tag was present, and inserted nothing. Every page
carried the arming half and none carried the running half.

That failure is invisible from outside. The head snippet arms a 2.5s failsafe
that strips the styles when window.__flow is unset, so with the script missing
the site looks *correct* — every block visible, nothing broken, just no
animation and no error. It was caught by printing window.__flow in a headless
run, not by looking at the page.

Three things must hold together, and any one alone is the broken state:

  1. assets/js/flow.js exists in the checkout        (link_check covers the
                                                      path; this covers the file)
  2. every page arms the styles  -> classList.add("js-reveal")
  3. every page loads the script -> <script src="/assets/js/flow.js"></script>

Gates. Deterministic, no network.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "assets" / "js" / "flow.js"
TAG = '<script src="/assets/js/flow.js"></script>'
ARM = 'classList.add("js-reveal")'


def sets_flag(js: str) -> bool:
    """Does flow.js actually ASSIGN window.__flow, in code?

    The obvious version of this — `"window.__flow" in js` — passed a mutant
    that had the assignment cut out, because the file's own header comment
    explains what window.__flow is for. That is the same mistake this whole
    file exists to catch, made one layer up. Comment lines are stripped first.
    """
    for line in js.splitlines():
        s = line.strip()
        if s.startswith(("*", "/*", "//", "*/")):
            continue
        if "window.__flow" in s and "=" in s.split("window.__flow", 1)[1]:
            return True
    return False


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts:
            continue
        yield p


def main():
    problems = []

    if not SCRIPT.is_file():
        problems.append(("assets/js/flow.js", "the script itself is missing"))
    elif not sets_flag(SCRIPT.read_text(encoding="utf-8")):
        # the head snippet's failsafe keys on this flag; without it the failsafe
        # fires on every load and the animation never survives past 2.5s
        problems.append(("assets/js/flow.js", "does not set window.__flow — "
                                              "the head failsafe will strip the styles on every load"))

    n = 0
    for p in pages():
        n += 1
        rel = p.relative_to(ROOT).as_posix()
        body = p.read_text(encoding="utf-8")
        armed, loaded = body.count(ARM), body.count(TAG)
        if armed != 1 or loaded != 1:
            problems.append((rel, f"arms x{armed}, loads x{loaded} — expected 1 and 1"))

    print(f"pages checked: {n}")
    for rel, why in problems:
        print(f"::error file={rel}::reveal wiring: {why}")

    if problems:
        print(f"\nFAIL: {len(problems)} reveal-wiring problem(s).")
        return 1
    print("OK: every page both arms and loads the reveal script.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
