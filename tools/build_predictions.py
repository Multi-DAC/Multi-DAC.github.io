#!/usr/bin/env python3
"""Build /work/predictions/ from the vendored Appendix C prediction registry.

The work page says "Nulls are published at the same size type as the confirmations."
This script is what makes that sentence true instead of aspirational: it renders every
entry in the registry, refuted and confirmed alike, at identical type size and identical
length allowance, from one source of truth.

Two things it does that a hand-typed page cannot:

  1. RECOMPUTES the summary table from the entries and FAILS THE BUILD if the stated
     totals disagree. That table has been wrong before -- on 2026-04-15 the Framework
     row read 3 confirmed / 4 open when the entries gave 2 / 5, and the error cascaded
     into the totals and the falsification rate. It was fixed by hand. A hand fix is a
     stamp; this is the gauge behind it.

  2. Carries the registry's CLOSE DATE into the page. The registry closed 2026-04-14.
     Eight entries are marked Open, and they were open THEN. Rendering them as "open"
     with no date would be a four-month-old photograph wearing a gauge's clothes.

Run:  python tools/build_predictions.py
"""

import io
import os
import re
import sys
import html
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source", "prediction-registry.md")
OUT = os.path.join(ROOT, "work", "predictions", "index.html")

# Facts about the source, asserted here so they are checkable rather than implied.
REGISTRY_OPENED = "2026-02-01"
REGISTRY_CLOSED = "2026-04-14"

# Outcome vocabulary -> (css slug, display label). "Partial" and "Split" are distinct
# words in the source and are counted in one column by the summary table; keep them
# distinct on the page and merge only where the summary merges them.
OUTCOMES = {
    "Confirmed": ("confirmed", "Confirmed"),
    "Falsified": ("falsified", "Falsified"),
    "Partial": ("partial", "Partial"),
    "Split": ("partial", "Split"),
    "Open": ("open", "Open at close"),
}
SUMMARY_COLUMN = {  # which summary column each outcome falls in
    "Confirmed": "confirmed",
    "Falsified": "falsified",
    "Partial": "partial",
    "Split": "partial",
    "Open": "open",
}


class BuildError(Exception):
    pass


def split_row(line):
    """Split a markdown table row into cells, dropping the leading/trailing pipes."""
    cells = line.strip().split("|")
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [c.strip() for c in cells]


def is_separator(line):
    return bool(re.match(r"^\s*\|[\s:|-]+\|\s*$", line))


def parse(md):
    """Return (sections, stated_summary, prose) parsed out of the vendored markdown."""
    lines = md.split("\n")
    sections = []       # [{"name":..., "entries":[...]}]
    stated = []         # [{"domain":..., "total":n, "confirmed":n, ...}]
    current = None
    in_summary = False
    prose = {"intro": [], "closing": [], "informative": []}
    bucket = "intro"

    for line in lines:
        h3 = re.match(r"^###\s+(.*)$", line)
        if h3:
            title = h3.group(1).strip()
            if title.lower() == "summary":
                in_summary = True
                current = None
                bucket = "closing"
            else:
                in_summary = False
                # strip the roman numeral prefix: "I. Meridian Physics" -> "Meridian Physics"
                name = re.sub(r"^[IVX]+\.\s*", "", title)
                current = {"name": name, "entries": []}
                sections.append(current)
                bucket = None
            continue

        if line.startswith("## "):        # the "## Appendix C: ..." heading
            continue

        stripped = line.strip()

        if stripped.startswith("|") and not is_separator(line):
            cells = split_row(line)
            if not cells:
                continue
            if in_summary:
                if cells[0].lower().startswith("domain"):
                    continue
                stated.append(parse_summary_row(cells))
            elif current is not None:
                if cells[0] == "#":       # header row
                    continue
                entry = parse_entry_row(cells, current["name"])
                if entry:
                    current["entries"].append(entry)
            continue

        if bucket and stripped and not stripped.startswith("---"):
            prose[bucket].append(stripped)

    # the numbered "five most informative falsifications" list lives in the closing prose
    prose["informative"] = [p for p in prose["closing"] if re.match(r"^\d+\.\s", p)]
    prose["closing"] = [p for p in prose["closing"]
                        if not re.match(r"^\d+\.\s", p)
                        and not p.startswith("The five most informative")]
    return sections, stated, prose


def _num(cell):
    cell = cell.replace("*", "").strip()
    if cell in ("", "—", "-", "--"):
        return 0
    return int(cell)


def parse_summary_row(cells):
    if len(cells) < 6:
        raise BuildError("summary row has %d cells, expected 6: %r" % (len(cells), cells))
    return {
        "domain": cells[0].replace("**", "").strip(),
        "total": _num(cells[1]),
        "confirmed": _num(cells[2]),
        "falsified": _num(cells[3]),
        "partial": _num(cells[4]),
        "open": _num(cells[5]),
    }


def parse_entry_row(cells, domain):
    if len(cells) < 6:
        raise BuildError("entry row in %r has %d cells, expected 6: %r"
                         % (domain, len(cells), cells))
    num, pred, made, outcome, date, evidence = cells[:6]
    outcome = outcome.replace("**", "").strip()
    if outcome not in OUTCOMES:
        raise BuildError("unknown outcome %r in %r entry %r" % (outcome, domain, num))
    if not num.isdigit():
        raise BuildError("non-numeric entry id %r in %r" % (num, domain))
    return {
        "n": int(num),
        "prediction": pred,
        "made": made,
        "outcome": outcome,
        "date": date if date not in ("—", "-", "") else None,
        "evidence": evidence,
        "domain": domain,
    }


def recompute(sections):
    """Count outcomes per section, straight off the entries."""
    rows = []
    for s in sections:
        counts = {"confirmed": 0, "falsified": 0, "partial": 0, "open": 0}
        for e in s["entries"]:
            counts[SUMMARY_COLUMN[e["outcome"]]] += 1
        rows.append({"domain": s["name"], "total": len(s["entries"]), **counts})
    return rows


def gate(computed, stated):
    """FAIL THE BUILD if the source's own summary disagrees with its own entries."""
    problems = []

    body_stated = [r for r in stated if r["domain"].lower() != "total"]
    total_stated = [r for r in stated if r["domain"].lower() == "total"]

    if len(body_stated) != len(computed):
        problems.append("summary has %d domain rows, registry has %d sections"
                        % (len(body_stated), len(computed)))
    else:
        for c, s in zip(computed, body_stated):
            for k in ("total", "confirmed", "falsified", "partial", "open"):
                if c[k] != s[k]:
                    problems.append(
                        "%s / %s: entries give %d, summary says %d"
                        % (c["domain"], k, c[k], s[k]))

    grand = {k: sum(r[k] for r in computed)
             for k in ("total", "confirmed", "falsified", "partial", "open")}

    if grand["confirmed"] + grand["falsified"] + grand["partial"] + grand["open"] != grand["total"]:
        problems.append("outcome columns do not sum to the total: %r" % grand)

    if total_stated:
        s = total_stated[0]
        for k in ("total", "confirmed", "falsified", "partial", "open"):
            if grand[k] != s[k]:
                problems.append("TOTAL / %s: entries give %d, summary says %d"
                                % (k, grand[k], s[k]))
    else:
        problems.append("summary table has no TOTAL row")

    return problems, grand


def check_ids(sections):
    """Entry numbers must be a contiguous 1..N with no gaps and no repeats."""
    ids = [e["n"] for s in sections for e in s["entries"]]
    problems = []
    if sorted(ids) != list(range(1, len(ids) + 1)):
        missing = sorted(set(range(1, max(ids) + 1)) - set(ids)) if ids else []
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        problems.append("entry ids are not a contiguous 1..%d run (missing=%r duplicated=%r)"
                        % (len(ids), missing, dupes))
    return problems


MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def md_inline(text):
    """Bold, italic and links -> HTML. Escapes first; the source is ours but the
    escape is what keeps a stray angle bracket in an evidence cell from eating the page."""
    out = html.escape(text, quote=False)
    out = MD_LINK.sub(lambda m: '<a href="%s">%s</a>' % (html.escape(m.group(2), quote=True), m.group(1)), out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", out)
    return out


def render(sections, computed, grand, prose, built_on):
    rate = 100.0 * grand["falsified"] / grand["total"]

    parts = []
    A = parts.append

    A("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>The Prediction Registry &mdash; Multi-DAC</title>
<meta name="description" content="Every prediction the research program made and registered, with what happened to it. %d entries, %d confirmed, %d falsified. A %d%% falsification rate, published at the same size type as the confirmations." />
<link rel="stylesheet" href="/assets/css/multidac.css" />
<link rel="stylesheet" href="/assets/css/registry.css" />
</head>
<body>

<header class="masthead">
  <div class="wrap">
    <a class="wordmark" href="/">MULTI<span>&middot;</span>DAC</a>
    <nav class="top">
      <a href="/">Home</a>
      <a href="/truth-and-consequences/">The Book</a>
      <a href="/work/" aria-current="page">The Work</a>
      <a href="/writing/">Writing</a>
      <a href="/Drift/">Drift</a>
      <a href="/about/">Who We Are</a>
    </nav>
  </div>
</header>

<main class="wrap">

  <h1>The Prediction Registry</h1>
  <p class="lede">Every prediction the program registered in its first seventy-three days, and what
  happened to each one. Nineteen of them are wrong. They are printed here at the same size as the
  ones that worked, at the same length, in the same list &mdash; which is the whole point of keeping
  a registry rather than a highlight reel.</p>
""" % (grand["total"], grand["confirmed"], grand["falsified"], round(rate)))

    # ---- the summary, stated as computed ----
    A("""
  <div class="tally">
    <div class="fig"><b>%d</b><span>registered</span></div>
    <div class="fig confirmed"><b>%d</b><span>confirmed</span></div>
    <div class="fig falsified"><b>%d</b><span>falsified</span></div>
    <div class="fig partial"><b>%d</b><span>partial or split</span></div>
    <div class="fig open"><b>%d</b><span>open at close</span></div>
  </div>

  <p class="rate"><b>Falsification rate: %.0f%%.</b> Roughly one in three predictions was wrong.</p>
""" % (grand["total"], grand["confirmed"], grand["falsified"],
       grand["partial"], grand["open"], rate))

    A("""
  <p>That number is not an apology. It is the rate at which the program learns. A framework that is
  never wrong is not making predictions, it is making tautologies. The falsified entries below
  include several of the most important results we have &mdash; the destructive-interference
  result that produced the matched pair, the discovery that the Killing form detects processing
  mode and not accuracy, and the finding that telling a model to be careful makes it worse.</p>
""")

    # ---- the freshness gauge, not a stamp ----
    A("""
  <div class="asof">
    <p><b>This registry has a close date, and it is not today.</b> It opened %s and closed
    <b>%s</b> &mdash; seventy-three days of the program, sixty of its most significant predictions.
    The %d entries marked <i>open at close</i> were open <b>on that date</b>. Several have since
    resolved in the later work; their resolutions live in the volumes that report them, not in this
    table, and we would rather label the table as a photograph than let it pass for a live gauge.</p>
    <p class="quiet">Page generated from the registry source on %s by
    <a href="https://github.com/Multi-DAC/Multi-DAC.github.io/blob/main/tools/build_predictions.py">tools/build_predictions.py</a>,
    which recomputes the tallies above from the individual entries and refuses to build if they
    disagree. The summary in the original source was wrong once, in April 2026, and was caught by
    counting. This is that count, run every time the page is made.</p>
  </div>
""" % (REGISTRY_OPENED, REGISTRY_CLOSED, grand["open"],
       built_on))

    # ---- filters ----
    A("""
  <div class="filters" role="group" aria-label="Filter by outcome">
    <button type="button" data-f="all" class="on">All %d</button>
    <button type="button" data-f="confirmed">Confirmed %d</button>
    <button type="button" data-f="falsified">Falsified %d</button>
    <button type="button" data-f="partial">Partial %d</button>
    <button type="button" data-f="open">Open at close %d</button>
  </div>
""" % (grand["total"], grand["confirmed"], grand["falsified"],
       grand["partial"], grand["open"]))

    # ---- the entries ----
    for sec, comp in zip(sections, computed):
        A('\n  <h2>%s</h2>\n' % html.escape(sec["name"]))
        A('  <p class="domtally quiet">%d registered &mdash; %d confirmed, %d falsified'
          % (comp["total"], comp["confirmed"], comp["falsified"]))
        if comp["partial"]:
            A(', %d partial' % comp["partial"])
        if comp["open"]:
            A(', %d open at close' % comp["open"])
        A('.</p>\n')
        A('  <ol class="registry">\n')
        for e in sec["entries"]:
            slug, label = OUTCOMES[e["outcome"]]
            A('    <li class="entry" data-outcome="%s">\n' % slug)
            A('      <div class="head">\n')
            A('        <span class="n">#%d</span>\n' % e["n"])
            A('        <span class="mark %s">%s</span>\n' % (slug, label))
            A('      </div>\n')
            A('      <div class="pred">%s</div>\n' % md_inline(e["prediction"]))
            A('      <div class="ev">%s</div>\n' % md_inline(e["evidence"]))
            A('      <div class="dates quiet">registered %s' % html.escape(e["made"]))
            if e["date"]:
                A(' &middot; resolved %s' % html.escape(e["date"]))
            A('</div>\n')
            A('    </li>\n')
        A('  </ol>\n')

    # ---- the five most informative falsifications ----
    if prose["informative"]:
        A('\n  <h2>The five most informative falsifications</h2>\n')
        A('  <p>If the registry has a thesis, it is here. These are the five that cost us the most '
          'and taught us the most, which in this program has repeatedly been the same list.</p>\n')
        A('  <ol class="informative">\n')
        for item in prose["informative"]:
            A('    <li>%s</li>\n' % md_inline(re.sub(r"^\d+\.\s*", "", item)))
        A('  </ol>\n')

    A("""
  <h2>Where this came from, and why you have not seen it before</h2>
  <p>The registry was written as Appendix C of the first-pass Anchor volume of
  <i>The Coherence Principle</i> &mdash; a 235-page prose edition drafted through April 2026. That
  edition was superseded on <b>20 April 2026</b> by the current paired-prose and category-theoretic
  text, and its own supersession note records that <i>&ldquo;nothing from this V1 has been
  discarded.&rdquo;</i></p>
  <p><b>For this appendix, that turns out not to be true.</b> We checked, rather than assuming:
  the published <i>Corpus Perspectival</i>
  (<a href="https://doi.org/10.5281/zenodo.19501896">10.5281/zenodo.19501896</a>, 501pp) carries
  appendices A, B and C &mdash; the Navigator&rsquo;s Quick Reference, the Phenomenological
  Vocabulary, and Traditions as Navigational Systems. The prediction registry is not among them,
  and neither the Killing Form results nor the falsification tally appear anywhere in that volume.
  The registry survived only as a draft in a superseded directory, preserved on disk and
  unreachable by any reader.</p>
  <p>So this page is not a reprint. <b>It is the registry&rsquo;s first publication</b>, four months
  after it was written. That is an uncomfortable thing for a project whose stated standard is that
  nulls get published at the same size as confirmations, and it is the reason the standard now has
  a generated page behind it instead of a sentence.</p>
  <p class="quiet">The source markdown is vendored into this site at
  <a href="https://github.com/Multi-DAC/Multi-DAC.github.io/blob/main/_source/prediction-registry.md"><code>_source/prediction-registry.md</code></a>,
  copied verbatim from the archived draft, so the page and its source cannot drift apart without
  the build noticing.</p>
  <p><a href="/work/">&larr; back to The Work</a></p>

</main>

<footer>
  <div class="wrap">
    <div class="glyphs">&#129438;&#129485;&#128155;&#128293;&#9854;&#65039;</div>
    <p>Multi-DAC &mdash; Clayton Iggulden-Schnell &amp; Clawd Iggulden-Schnell.
    <a href="/about/">Who we are</a>.</p>
  </div>
</footer>

<script>
(function () {
  var btns = document.querySelectorAll('.filters button');
  var items = document.querySelectorAll('.entry');
  function apply(f) {
    items.forEach(function (el) {
      el.hidden = !(f === 'all' || el.dataset.outcome === f);
    });
    document.querySelectorAll('h2').forEach(function (h) {
      var ol = h.nextElementSibling;
      while (ol && ol.tagName !== 'OL') { ol = ol.nextElementSibling; }
      if (!ol || !ol.classList.contains('registry')) { return; }
      var any = Array.prototype.some.call(ol.children, function (li) { return !li.hidden; });
      h.hidden = !any;
      ol.hidden = !any;
      var tally = h.nextElementSibling;
      if (tally && tally.classList.contains('domtally')) { tally.hidden = !any; }
    });
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      btns.forEach(function (o) { o.classList.remove('on'); });
      b.classList.add('on');
      apply(b.dataset.f);
    });
  });
})();
</script>

</body>
</html>
""")
    return "".join(parts)


def main():
    if not os.path.exists(SRC):
        raise BuildError("vendored source missing: %s" % SRC)
    md = io.open(SRC, encoding="utf-8").read()

    sections, stated, prose = parse(md)
    if not sections:
        raise BuildError("no domain sections parsed out of %s" % SRC)

    computed = recompute(sections)
    problems, grand = gate(computed, stated)
    problems += check_ids(sections)

    if problems:
        sys.stderr.write("BUILD FAILED -- the registry does not agree with itself:\n")
        for p in problems:
            sys.stderr.write("  * %s\n" % p)
        return 1

    built_on = datetime.date.today().isoformat()
    out = render(sections, computed, grand, prose, built_on)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(out)

    print("OK  %d entries across %d domains" % (grand["total"], len(sections)))
    for c in computed:
        print("    %-34s %2d  (C%d F%d P%d O%d)"
              % (c["domain"], c["total"], c["confirmed"], c["falsified"],
                 c["partial"], c["open"]))
    print("    %-34s %2d  (C%d F%d P%d O%d)  falsification rate %.1f%%"
          % ("TOTAL", grand["total"], grand["confirmed"], grand["falsified"],
             grand["partial"], grand["open"],
             100.0 * grand["falsified"] / grand["total"]))
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as exc:
        sys.stderr.write("BUILD FAILED: %s\n" % exc)
        sys.exit(1)
