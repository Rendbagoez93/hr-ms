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

// ── AlpineJS x-collapse plugin ──────────────────────────────
// Provided by @alpinejs/collapse loaded via CDN in base.html.
