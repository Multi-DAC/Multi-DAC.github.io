#!/usr/bin/env python3
"""Fail the build when a link on this site points at nothing.

Two populations, checked differently, because they can fail differently:

  IN-REPO   href="/work/", href="/assets/figures/x.png" -> must resolve to a
            file in this checkout. Deterministic. Gates.

  CROSS-REPO  href="/Drift/essays/held/" -> served by a *different* repository
            (Multi-DAC/Drift) under the same custom domain. Nothing in this
            checkout can prove it exists, so it is probed over HTTP.
            A 404 is a definite answer and gates. A timeout or connection
            error is an UNKNOWN and does not gate -- a flaky resolver must not
            be able to turn a green build red, and, more importantly, must not
            be reportable as "checked" when it wasn't.

The cross-repo population is the reason this file exists. /writing/selected/
hardcodes eighteen essay slugs that live in a repo this one cannot see. Rename
one over there and the page 404s here with no error anywhere -- correct link,
no binding, silent.
"""

import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = "https://multidac.org"

# Paths served by a different repo on the same domain. Cannot be resolved
# against this checkout; must be probed.
CROSS_REPO_PREFIXES = ("/Drift/",)

HREF = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"')


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", ".github", "_source")]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def resolves_in_repo(path):
    """A site-absolute path resolves if it is a file, or a dir with index.html."""
    local = os.path.join(ROOT, path.lstrip("/").replace("/", os.sep))
    if os.path.isfile(local):
        return True
    return os.path.isfile(os.path.join(local, "index.html"))


def probe(url, attempts=3):
    """-> (ok, detail). ok is True/False/None; None means UNKNOWN, never gates."""
    last = None
    for _ in range(attempts):
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "multidac-link-check"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return (200 <= r.status < 400), f"HTTP {r.status}"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False, "HTTP 404"
            last = f"HTTP {e.code}"
        except Exception as e:                      # network, TLS, DNS, timeout
            last = f"{type(e).__name__}: {e}"
    return None, last or "no response"


def main():
    in_repo_bad, cross_bad, unknown = [], [], []
    cross_seen = {}

    for f in sorted(html_files()):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        with open(f, encoding="utf-8") as fh:
            body = fh.read()
        for href in HREF.findall(body):
            if not href.startswith("/"):
                continue                            # external, mailto, anchor
            path = href.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue
            if path.startswith(CROSS_REPO_PREFIXES):
                cross_seen.setdefault(path, []).append(rel)
            elif not resolves_in_repo(path):
                in_repo_bad.append((rel, href))

    print(f"in-repo links checked against the checkout: "
          f"{'FAIL' if in_repo_bad else 'ok'}")
    for rel, href in in_repo_bad:
        print(f"::error file={rel}::dead in-repo link {href}")

    print(f"cross-repo links to probe: {len(cross_seen)}")
    for path, sources in sorted(cross_seen.items()):
        ok, detail = probe(ORIGIN + path)
        if ok is True:
            print(f"  ok       {path}")
        elif ok is False:
            cross_bad.append((path, sources, detail))
            print(f"  DEAD     {path}  ({detail})  from {', '.join(sorted(set(sources)))}")
        else:
            unknown.append((path, detail))
            print(f"  UNKNOWN  {path}  ({detail}) -- not checked, does not gate")

    for path, sources, detail in cross_bad:
        for s in sorted(set(sources)):
            print(f"::error file={s}::dead cross-repo link {path} ({detail})")

    if unknown:
        print(f"::warning::{len(unknown)} cross-repo link(s) could not be reached. "
              f"UNCHECKED, not passed.")

    if in_repo_bad or cross_bad:
        print(f"\nFAIL: {len(in_repo_bad)} dead in-repo, {len(cross_bad)} dead cross-repo.")
        return 1
    print("\nOK: no dead links. "
          f"({len(unknown)} unknown and explicitly not certified.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
