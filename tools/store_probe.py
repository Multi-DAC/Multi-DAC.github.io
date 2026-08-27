#!/usr/bin/env python3
"""Probe every outbound store link on this site and report whether a buyer
could actually complete a purchase.

WHY THIS EXISTS
---------------
On 2026-08-27 the Payhip storefront for Truth and Consequences returned HTTP
200, rendered correctly, and carried this in its own machine-readable product
record:

    "offers": {"@type": "Offer", "price": "9.99",
               "availability": "InStock", "priceCurrency": "USD"}

while the visible page said, in place of the buy button:

    "Seller is unable to receive payments since their PayPal or Stripe
     account has not yet been connected."

The structured field a checker would naturally trust said InStock. Checkout was
impossible. A status-code check, a link check, and a schema.org availability
check would each have passed. So this probe deliberately does NOT read
schema.org availability, and it looks for the blocker in the rendered page.

WHAT A PASS MEANS
-----------------
"No known blocker found, on a page that proved it was the product page" —
nothing stronger. The blocker list below is a denylist, which encodes only the
failures already met. A store can break in a way not listed here and this probe
will say nothing. It is a tripwire, not a proof of sale.

The positive marker is not decoration. The first run of this script reported
`ok` for the Amazon listing. Amazon had served a 3.7 KB anti-bot page: HTTP
200, no product, no price, no title — and therefore none of the blocker strings
either. Absence of a known failure is not evidence of success when the body
handed back is not the page you asked for. So a URL must now show its own
product title before any verdict is issued; if it does not, the result is
NO VERDICT, which is a distinct outcome from a pass.

The Payhip account was connected to Stripe later the same day, and that fix is
what exposed the next weakness: a denylist can only ever report "no failure I
already know about". Where a host states the good case in its own words —
Payhip emits `hasConnectedPaymentProvider` as true or false, not only on
failure — the true value is now REQUIRED (see REQUIRED_POSITIVE). If the field
moves or vanishes the result is NO VERDICT, not a pass. Both arms are exercised
by mutating a captured page: flag→false must report BLOCKED, flag removed must
report NO VERDICT.

NEVER GATES. Same reasoning as the DNS step in domain-guard: an outbound
network check that fails the build on a flaky third party trains you to ignore
red. It prints, and CI keeps going.
"""

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")

# Hosts we sell through. Anything else linked from a .buy row is ignored.
STORE_HOSTS = ("payhip.com", "gumroad.com", "amazon.com")

# A response must carry this before any verdict is issued. Without it we were
# handed a bot wall, an interstitial, or an error skin — not the listing.
PRODUCT_MARKER = r"Truth and Consequences"

# Where a host publishes a POSITIVE statement that it can take money, require
# it. This is the difference between "I found no failure I know about" and "the
# store said, in its own words, that it is able to charge a card". Payhip emits
# the flag either way, so the true case is checkable and absence is meaningful.
# A host with no entry here still falls back to the denylist below, which is
# weaker on purpose — the weakness is stated in the output, not hidden.
REQUIRED_POSITIVE = {
    "payhip.com": (r'"hasConnectedPaymentProvider"\s*:\s*true',
                   "Payhip reports a connected payment provider"),
}

# (regex, what it means). Case-insensitive, matched against the fetched body.
BLOCKERS = [
    (r"unable to receive payments",
     "seller has no payment provider connected"),
    (r'"hasConnectedPaymentProvider"\s*:\s*false',
     "Payhip reports no connected payment provider"),
    (r"this product is no longer available",
     "product delisted"),
    (r"currently unavailable",
     "listing reports itself unavailable"),
]


def store_links():
    """Every store URL appearing inside a <div class="buy"> block."""
    found = {}
    for page in sorted(ROOT.rglob("index.html")):
        if ".git" in page.parts or "_source" in page.parts:
            continue
        html = page.read_text(encoding="utf-8")
        for block in re.findall(r'<div class="buy">(.*?)</div>', html, re.S):
            for url in re.findall(r'href="(https?://[^"]+)"', block):
                if any(h in url for h in STORE_HOSTS):
                    found.setdefault(url, []).append(
                        "/" + page.relative_to(ROOT).parent.as_posix().strip("."))
    return found


def probe(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:                                  # noqa: BLE001
        return None, f"__unreachable__ {e}"


def main():
    links = store_links()
    if not links:
        print("store-probe: no store links found in any .buy block "
              "— that is itself worth a look")
        return 0

    hits = 0
    silent = 0
    for url, pages in sorted(links.items()):
        status, body = probe(url)
        if status is None:
            silent += 1
            print(f"  ?  {url}\n     NO VERDICT — unreachable ({body[:100]})")
            continue
        if not re.search(PRODUCT_MARKER, body, re.I):
            silent += 1
            print(f"  ?  {url}")
            print(f"     NO VERDICT — HTTP {status} but the body ({len(body)} B) "
                  f"does not contain {PRODUCT_MARKER!r}. Bot wall or "
                  f"interstitial; blocker checks were NOT meaningfully run.")
            continue
        found = [why for pat, why in BLOCKERS if re.search(pat, body, re.I)]
        if found:
            hits += 1
            print(f"  X  {url}")
            for why in found:
                print(f"     BLOCKED: {why}")
            print(f"     linked from: {', '.join(sorted(set(pages)))}")
            continue

        want = next((v for h, v in REQUIRED_POSITIVE.items() if h in url), None)
        if want is None:
            print(f"  ok {url}  (HTTP {status}, product page confirmed, "
                  f"no known blocker — denylist only, not proof of sale)")
        elif re.search(want[0], body, re.I):
            print(f"  OK {url}  (HTTP {status}, product page confirmed, "
                  f"{want[1]})")
        else:
            silent += 1
            print(f"  ?  {url}")
            print(f"     NO VERDICT — HTTP {status}, product page confirmed, "
                  f"no known blocker, but the positive marker "
                  f"({want[1]}) is ABSENT. Either the store cannot charge or "
                  f"the field moved. Absence of the failure is not a pass.")

    if hits:
        print(f"\nstore-probe: {hits} store link(s) a buyer cannot complete. "
              "Reported, not gating — fix the store, not this script.")
    if silent:
        print(f"store-probe: {silent} link(s) returned NO VERDICT. "
              "That is not a pass and must not be read as one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
