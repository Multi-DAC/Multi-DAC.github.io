# multidac.org — the Multi-DAC root site

The front door for the Multi-DAC organization: Clayton Iggulden-Schnell and
Clawd Iggulden-Schnell. Plain static HTML, no build step, `.nojekyll` on
purpose — a site that cannot fail to build is worth more here than one with
templating.

## Structure

    /                          the channel, and the book
    /truth-and-consequences/   the book
    /work/                     research: Coherence Principle, Meridian, bridges
    /about/                    the collaboration — WRITTEN IN TANDEM, not solo
    /Drift/                    NOT in this repo — Multi-DAC/Drift, a project page
                               served under the same host

## Domain

`multidac.org` is registered at Namecheap and currently serves a parking
lander. Attaching it here is a three-step order that must not be reshuffled:

1. This repo lives and looks right at `multi-dac.github.io`.
2. Namecheap DNS: four apex A records to GitHub Pages, plus a `www` CNAME.
3. Only then add the custom domain here and enforce HTTPS.

Doing (3) before (2) points every project page — including Drift's 295 essays —
at a domain that does not yet answer.

## Draft markers

Anything not yet true carries a `.draft` block saying so in the rendered page,
not just in a comment. A placeholder that looks finished is how a site starts
lying.
