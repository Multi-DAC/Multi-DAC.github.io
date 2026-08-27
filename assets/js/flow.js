/* multidac.org — reveal-on-scroll.
 *
 * The only JavaScript on the site, and it is allowed to do exactly one thing:
 * fade blocks in as they enter the viewport. Everything the reader came for is
 * in the HTML and is readable with this file blocked, missing, or broken.
 *
 * The hiding is done by CSS gated on html.js-reveal, which an inline snippet in
 * each page's <head> sets before first paint. That ordering is the whole risk:
 * if THIS file 404s or throws, the class is already on and every .reveal block
 * stays invisible forever, with no error anywhere a reader could see. So the
 * head snippet arms a 2.5s failsafe that strips the class unless window.__flow
 * says this file actually ran. The flag below is the other half of that pair —
 * do not remove it without removing the failsafe.
 */
(function () {
  "use strict";

  window.__flow = true;

  var els = document.querySelectorAll(".reveal");
  if (!els.length) return;

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function showAll() {
    for (var i = 0; i < els.length; i++) els[i].classList.add("seen");
  }

  if (reduce || !("IntersectionObserver" in window)) {
    showAll();
    return;
  }

  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("seen");
        io.unobserve(e.target);
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.04 }
  );

  for (var i = 0; i < els.length; i++) {
    // anything already on screen at load reveals immediately rather than
    // waiting for a scroll that may never come on a short page
    io.observe(els[i]);
  }

  // last resort: if something goes wrong and blocks are still hidden after
  // three seconds, show them. A page that swallows its own text is worse
  // than a page with no animation.
  setTimeout(showAll, 3000);
})();
