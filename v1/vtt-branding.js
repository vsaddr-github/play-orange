/* vtt-branding.js · VLAD'S TEST TARGET
 * ─────────────────────────────────────────────────────────────────────────
 * Fetches vtt-header.html and vtt-footer.html from the same folder and
 * injects them into every graph page.
 *
 * Works on GitHub Pages (static hosting) — uses plain fetch() with a
 * relative URL so it resolves correctly whether the pages are served from
 * the repo root or a subfolder.
 *
 * USAGE — add these two lines to each graph HTML file:
 *
 *   In <head> or just before </head>:
 *     <script src="vtt-branding.js" defer></script>
 *
 *   As the first element inside <body>:
 *     <div id="vtt-header-mount"></div>
 *
 *   As the last element inside <body> (before closing </body>):
 *     <div id="vtt-footer-mount"></div>
 *
 * The script resolves the path to the partials relative to its own URL,
 * so it works regardless of which subdirectory the graph files are in,
 * as long as vtt-header.html and vtt-footer.html are in the same folder.
 * ─────────────────────────────────────────────────────────────────────────
 */

(function () {
  'use strict';

  /* ── resolve base path ───────────────────────────────────────────────────
   * Find this script's own src URL and strip the filename to get the
   * directory. This makes the loader folder-agnostic. */
  function getBasePath() {
    const scripts = document.querySelectorAll('script[src]');
    for (const s of scripts) {
      if (s.src && s.src.includes('vtt-branding')) {
        return s.src.replace(/vtt-branding\.js.*$/, '');
      }
    }
    /* fallback: same directory as the page */
    return window.location.href.replace(/[^/]+$/, '');
  }

  const base = getBasePath();

  /* ── fetch and inject a partial into a mount point ───────────────────────
   * id     — the id of the mount <div>
   * file   — filename of the partial (e.g. 'vtt-header.html')
   * insert — 'afterbegin' inserts at top of mount; 'beforeend' at bottom
   *          We actually replace the mount div entirely for clean DOM. */
  function injectPartial(id, file, position) {
    const mount = document.getElementById(id);
    if (!mount) return Promise.resolve();   /* mount point missing — skip silently */

    const url = base + file;

    return fetch(url)
      .then(function (res) {
        if (!res.ok) throw new Error('vtt-branding: could not fetch ' + url + ' (' + res.status + ')');
        return res.text();
      })
      .then(function (html) {
        /* Insert the fetched HTML adjacent to the mount point,
         * then remove the placeholder div so it leaves no trace. */
        mount.insertAdjacentHTML(position, html);
        mount.parentNode.removeChild(mount);
      })
      .catch(function (err) {
        /* Non-fatal — page still works without branding if files are missing */
        console.warn(err.message);
      });
  }

  /* ── body padding ────────────────────────────────────────────────────────
   * Ensure the page content between header and footer has comfortable
   * horizontal padding matching the header/footer inner max-width constraint. */
  function addBodyPadding() {
    const style = document.createElement('style');
    style.textContent = [
      '/* vtt-branding.js — body content padding */',
      'body > *:not(.vtt-header):not(.vtt-footer):not(script):not(style) {',
      '  max-width: 920px;',
      '  margin-left:  auto;',
      '  margin-right: auto;',
      '  padding-left:  28px;',
      '  padding-right: 28px;',
      '}'
    ].join('\n');
    document.head.appendChild(style);
  }

  /* ── run ─────────────────────────────────────────────────────────────────
   * Inject header first (it declares the :root CSS variables that the
   * footer stylesheet depends on), then inject footer. */
  function run() {
    /* Header: insert BEFORE the mount div — it becomes the first child of body */
    injectPartial('vtt-header-mount', 'vtt-header.html', 'beforebegin')
      .then(function () {
        /* Footer: insert AFTER the mount div — becomes last child of body */
        return injectPartial('vtt-footer-mount', 'vtt-footer.html', 'afterend');
      });

    addBodyPadding();
  }

  /* Run after DOM is ready */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }

}());
