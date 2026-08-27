#!/usr/bin/env python3
"""Fail if one product is advertised at two different prices.

Why this exists
---------------
The price of Truth and Consequences is written into the page *text*, in a
<span class="price">, once per storefront link, across more than one file.
Change it in one place and the site quietly lies about its own price on the
other page. Nothing about that looks broken — it renders fine, it links fine,
and the wrong number is the one the reader sees first.

So this is a gauge that fails on its own rather than a note asking someone to
remember. It is scoped to a *product*, not to the site: prices are only
compared against other prices sitting in a `<div class="buy">` block that
carries the same product key (the Amazon ASIN). A future second book with its
own price is a different key and is not compared against this one.

Exit 1 on disagreement. Exit 1 if no priced block is found at all — an empty
sweep passing green is the failure mode this whole file is about.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BUY_BLOCK = re.compile(r'<div class="buy">(.*?)</div>', re.S)
PRICE = re.compile(r'<span class="price">\s*(?:&mdash;|—|-)?\s*\$([0-9]+(?:\.[0-9]{2})?)')
ASIN = re.compile(r'amazon\.com/dp/([A-Z0-9]{10})')


def main() -> int:
    # product key -> list of (price, file, storefront-ish context)
    seen: dict[str, list[tuple[str, str]]] = {}

    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding="utf-8", errors="replace")
        for block in BUY_BLOCK.findall(html):
            key_m = ASIN.search(block)
            if not key_m:
                continue
            key = key_m.group(1)
            for price in PRICE.findall(block):
                seen.setdefault(key, []).append((price, rel))

    if not seen:
        print("::error::price_parity found no priced buy-block at all. "
              "Either the markup changed or the sweep is broken — an empty "
              "pass is not a pass.")
        return 1

    failed = False
    for key, hits in sorted(seen.items()):
        prices = {p for p, _ in hits}
        where = ", ".join(f"${p} in {f}" for p, f in hits)
        if len(prices) > 1:
            failed = True
            print(f"::error::product {key} is advertised at "
                  f"{len(prices)} different prices: {where}")
        else:
            print(f"ok: product {key} = ${prices.pop()} "
                  f"across {len(hits)} link(s) [{where}]")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
