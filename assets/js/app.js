/**
 * HR-MS — Application JavaScript
 *
 * HTMX and AlpineJS are loaded via CDN in base.html.
 * This file contains project-level enhancements only.
 */

// ── HTMX global configuration ────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  // Automatically add loading indicator class on HTMX requests
  document.body.addEventListener("htmx:beforeRequest", (e) => {
    const el = e.detail.elt;
    el.classList.add("htmx-loading");
  });

  document.body.addEventListener("htmx:afterRequest", (e) => {
    const el = e.detail.elt;
    el.classList.remove("htmx-loading");
  });

  // Show toast for HTMX errors
  document.body.addEventListener("htmx:responseError", () => {
    console.error("HTMX request failed");
  });
});

// ── AlpineJS x-collapse plugin (minimal inline) ──────────────
// Provides x-collapse directive used in sidebar accordion groups.
document.addEventListener("alpine:init", () => {
  Alpine.directive("collapse", (el, { modifiers }) => {
    el._x_isCollapsible = true;

    const setDisplay = (open) => {
      if (open) {
        el.style.display = "";
        el.style.overflow = "hidden";
        const height = el.scrollHeight;
        el.style.height = "0px";
        requestAnimationFrame(() => {
          el.style.transition = "height 0.2s ease";
          el.style.height = height + "px";
          el.addEventListener(
            "transitionend",
            () => {
              el.style.height = "";
              el.style.overflow = "";
              el.style.transition = "";
            },
            { once: true }
          );
        });
      } else {
        el.style.overflow = "hidden";
        el.style.height = el.scrollHeight + "px";
        requestAnimationFrame(() => {
          el.style.transition = "height 0.2s ease";
          el.style.height = "0px";
          el.addEventListener(
            "transitionend",
            () => {
              el.style.display = "none";
              el.style.overflow = "";
              el.style.transition = "";
            },
            { once: true }
          );
        });
      }
    };

    // Watch via MutationObserver for x-show changes applied by Alpine
    const observer = new MutationObserver(() => {
      const isHidden = el.style.display === "none";
      setDisplay(!isHidden && el.offsetParent !== null);
    });
    observer.observe(el, { attributes: true, attributeFilter: ["style"] });
  });
});
