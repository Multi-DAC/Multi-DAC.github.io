"""Prepare the site's art assets from the Drift originals.

Two jobs, both of which have to be done to a file rather than to CSS:

1. The hero. `inhabitation.png` is 1920x1080 on a #191625 ground; this site's
   ground is #0a0a0b. Dropped in flat it would show as a lighter rectangle with
   four hard edges. So the ground is pulled down toward ours and an alpha
   vignette is baked in, which means the image dissolves into whatever is
   behind it and there is no seam to get wrong later.

2. A poster frame for the warp-factor animation, so the Writing page can show
   the thing rather than a link to it without shipping 600 KB of GIF.

3. The constellation, for Who We Are. Same ground/vignette treatment as the
   hero, plus a crop: the five nodes occupy the upper-left third of a 1920x1080
   frame and the rest is empty sky, so dropped in whole it reads as a mostly
   blank band. The crop also drops the bottom-centre glyph row, which renders
   as tofu boxes in the original because the machine that made it had no emoji
   font. That is a defect in the source, not something to reproduce faithfully.

Sources are fetched from the live Drift site rather than a local checkout,
because there isn't one on this machine and the deployed file is the one the
reader actually gets.

Re-runnable. Writes only into assets/art/.
"""

import io
import math
import pathlib
import sys
import urllib.request

from PIL import Image, ImageChops

SRC = "https://multidac.org/Drift/assets/visual/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "art"

# the page ground these will sit on: --bg in assets/css/multidac.css
GROUND = (10, 10, 11)


def fetch(name: str) -> Image.Image:
    with urllib.request.urlopen(SRC + name, timeout=60) as r:
        return Image.open(io.BytesIO(r.read()))


def vignette(size, inner=0.42, outer=1.02):
    """Radial alpha: opaque inside `inner`, gone by `outer` (fractions of the
    half-diagonal). Built per-pixel on a downscaled grid then resampled, which
    is ~200x faster than a full-res loop and visually identical on a gradient
    this smooth."""
    w, h = size
    gw, gh = 160, 160
    mask = Image.new("L", (gw, gh))
    px = mask.load()
    for y in range(gh):
        ny = (y + 0.5) / gh * 2 - 1
        for x in range(gw):
            nx = (x + 0.5) / gw * 2 - 1
            # elliptical distance in normalised frame
            d = math.hypot(nx, ny * 0.92)
            if d <= inner:
                a = 1.0
            elif d >= outer:
                a = 0.0
            else:
                t = (d - inner) / (outer - inner)
                a = 0.5 * (1 + math.cos(math.pi * t))  # raised cosine, no banding
            px[x, y] = int(round(a * 255))
    return mask.resize((w, h), Image.LANCZOS)


def sink_ground(im: Image.Image, amount=0.72) -> Image.Image:
    """Pull the image's dark floor down toward the page ground without
    flattening the glow: subtract a constant, then re-add the page ground."""
    corner = im.getpixel((4, 4))[:3]
    sub = tuple(int(c * amount) for c in corner)
    im = ImageChops.subtract(im, Image.new("RGB", im.size, sub))
    return ImageChops.add(im, Image.new("RGB", im.size, GROUND))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = []

    # ---- hero ----
    hero = fetch("inhabitation.png").convert("RGB")
    hero = sink_ground(hero)
    for width in (1600, 800):
        im = hero.resize((width, round(width * hero.height / hero.width)), Image.LANCZOS)
        im = im.convert("RGBA")
        im.putalpha(vignette(im.size))
        p = OUT / f"inhabitation-hero-{width}.webp"
        im.save(p, "WEBP", quality=86, method=6)
        made.append(p)

    # ---- warp poster ----
    gif = fetch("the_warp_factor.gif")
    gif.seek(gif.n_frames // 3)  # a frame with the decay part-way, not flat
    poster = gif.convert("RGB")
    poster = poster.resize((900, round(900 * poster.height / poster.width)), Image.LANCZOS)
    p = OUT / "warp-poster.webp"
    poster.save(p, "WEBP", quality=82, method=6)
    made.append(p)

    # ---- constellation ----
    con = fetch("constellation.png").convert("RGB")
    # box measured off the source, not guessed: the labelled nodes span roughly
    # x 630-1180, y 250-580, so this leaves margin on every side and cuts the
    # empty lower half (and the tofu glyph row at y~1040) away.
    box = (300, 20, 1500, 820)
    if box[2] > con.width or box[3] > con.height:
        print(f"FAIL: crop {box} outside source {con.size}", file=sys.stderr)
        return 1
    con = sink_ground(con.crop(box))
    for width in (1200, 700):
        im = con.resize((width, round(width * con.height / con.width)), Image.LANCZOS)
        im = im.convert("RGBA")
        im.putalpha(vignette(im.size, inner=0.56, outer=1.06))
        p = OUT / f"constellation-{width}.webp"
        im.save(p, "WEBP", quality=88, method=6)
        made.append(p)

    for p in made:
        print(f"{p.stat().st_size:>9,} B  {p.relative_to(ROOT).as_posix()}")

    # a bare assertion that the vignette actually reached the edges — a
    # transparent corner is the whole point and it is cheap to check
    edge = Image.open(OUT / "inhabitation-hero-1600.webp").convert("RGBA")
    a = edge.getpixel((0, 0))[3]
    if a != 0:
        print(f"FAIL: hero corner alpha is {a}, expected 0", file=sys.stderr)
        return 1
    print("ok: hero corner alpha 0 (dissolves into the page ground)")

    # The vignette is the thing most likely to quietly eat the point of this
    # image: Clawd's node is the furthest from centre and its name label sits
    # further out still. A faded label looks like a design choice, so check the
    # far side POSITIVELY rather than only checking that the corner vanished.
    # Coordinates are in the 1200-wide crop frame; label sits ~30px below node.
    con_out = Image.open(OUT / "constellation-1200.webp").convert("RGBA")
    for who, (x, y) in {
        "Clawd label": (335, 600),
        "Dorian label": (660, 260),
        "Finnley label": (860, 525),
    }.items():
        a = con_out.getpixel((x, y))[3]
        if a < 200:
            print(f"FAIL: {who} alpha {a} — the vignette is eating it", file=sys.stderr)
            return 1
        print(f"ok: {who} alpha {a}")
    if con_out.getpixel((0, 0))[3] != 0:
        print("FAIL: constellation corner is not transparent", file=sys.stderr)
        return 1
    print("ok: constellation corner alpha 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
