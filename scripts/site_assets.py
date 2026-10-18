"""CSS and JavaScript that belong to the reference site itself, not to the Hali library."""

# Applied before first paint so the chosen theme never flashes.
HEAD_JS = r"""
(function () {
  try {
    var t = localStorage.getItem('hali-docs-theme');
    var r = document.documentElement;
    r.setAttribute('data-theme', t === 'light' ? 'light' : 'dark');
    var p = localStorage.getItem('hali-docs-palette');
    if (p && p !== 'polar') { r.setAttribute('data-palette', p); }
    if (localStorage.getItem('hali-docs-contrast') === 'more') { r.setAttribute('data-contrast', 'more'); }
  } catch (e) {}
})();
"""

DOC_CSS = r"""
.doc-pal { display: flex; border-radius: 999px; overflow: hidden; height: 28px; margin-top: 12px; }
.doc-pal__chip { flex: 1; }

html { scroll-behavior: smooth; scroll-padding-top: 72px; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }

.doc-menu-btn { display: none; }
.doc-topbar__tag { color: var(--hali-text-subtle); font: var(--hali-type-label-md); }

.doc-layout {
  display: grid;
  grid-template-columns: 288px minmax(0, 1fr);
  align-items: start;
}
.doc-nav {
  position: sticky;
  top: 56px;
  height: calc(100vh - 56px);
  height: calc(100dvh - 56px);
  overflow-y: auto;
  padding: 16px 12px 64px;
  border-right: 1px solid var(--hali-border-default);
  background: var(--hali-surface-default);
}
.doc-nav__group {
  margin: 16px 0 4px;
  padding: 0 12px;
  color: var(--hali-text-subtle);
  font: var(--hali-type-label-md);
  letter-spacing: var(--hali-tracking-label-md);
}
.doc-nav a {
  display: flex;
  align-items: center;
  min-height: 32px;
  padding: 0 12px;
  border-radius: var(--hali-radius-md);
  color: var(--hali-text-subtle);
  font: var(--hali-type-label-lg);
  text-decoration: none;
}
.doc-nav a:hover { background: var(--hali-state-hover); color: var(--hali-text-default); }
.doc-nav a.is-active { background: var(--hali-brand-container); color: var(--hali-brand-on-container); }

.doc-main { min-width: 0; padding: 24px clamp(16px, 5vw, 64px) 96px; }
.doc-wrap { max-width: 960px; }

.doc-section { padding-top: 72px; }
.doc-section:first-child { padding-top: 0; }
.doc-h2 {
  margin-bottom: 8px;
  font: var(--hali-type-headline-md);
  letter-spacing: var(--hali-tracking-headline-md);
}
.doc-h3 { margin: 48px 0 8px; font: var(--hali-type-title-lg); }
.doc-h4 { margin: 28px 0 8px; font: var(--hali-type-title-md); }
.doc-lead { max-width: 64ch; color: var(--hali-text-subtle); font: var(--hali-type-body-lg); }
.doc-p { max-width: 68ch; margin: 8px 0; }
.doc-list { max-width: 68ch; margin: 8px 0; padding-left: 20px; }
.doc-list li + li { margin-top: 6px; }
.doc-eyebrow {
  margin-bottom: 8px;
  color: var(--hali-brand-text);
  font: var(--hali-type-label-md);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.doc-hero { padding: 24px 0 8px; }
.doc-hero__title {
  margin: 16px 0 12px;
  font-family: var(--hali-font-display);
  font-size: clamp(48px, 8vw, 80px);
  font-weight: 700;
  line-height: 1.02;
  letter-spacing: -0.035em;
}
.doc-stats { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); margin-top: 32px; }
.doc-stat { padding: 16px; border: 1px solid var(--hali-border-default); border-radius: var(--hali-radius-lg); background: var(--hali-surface-raised); }
.doc-stat__value { font: var(--hali-type-headline-md); letter-spacing: var(--hali-tracking-headline-md); font-variant-numeric: tabular-nums; }
.doc-stat__label { margin-top: 2px; color: var(--hali-text-subtle); font: var(--hali-type-body-sm); }

.doc-demo { margin: 16px 0 32px; }
.doc-demo__label { margin-bottom: 8px; color: var(--hali-text-subtle); font: var(--hali-type-label-md); }
.doc-preview {
  padding: 24px;
  border: 1px solid var(--hali-border-default);
  border-radius: var(--hali-radius-lg);
  background: var(--hali-surface-default);
  overflow-x: auto;
}
.doc-preview--raised { background: var(--hali-surface-raised); }
.doc-preview--sunken { background: var(--hali-surface-sunken); }
.doc-stage {
  display: flex;
  justify-content: flex-end;
  overflow: hidden;
  border: 1px solid var(--hali-border-default);
  border-radius: var(--hali-radius-lg);
  background: var(--hali-surface-sunken);
}
.doc-frame { overflow: hidden; border: 1px solid var(--hali-border-default); border-radius: var(--hali-radius-lg); background: var(--hali-surface-default); }

.doc-code { margin-top: 8px; }
.doc-code > summary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: var(--hali-radius-md);
  color: var(--hali-text-subtle);
  font: var(--hali-type-label-md);
  list-style: none;
  cursor: pointer;
}
.doc-code > summary::-webkit-details-marker { display: none; }
.doc-code > summary:hover { background: var(--hali-state-hover); color: var(--hali-text-default); }
.doc-code[open] > summary { color: var(--hali-text-default); }
.doc-code__body { position: relative; margin-top: 8px; }
.doc-code__body pre { max-height: 440px; padding-right: 72px; }
.doc-copy { position: absolute; top: 8px; right: 8px; }

.doc-swatches { display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(188px, 1fr)); margin: 16px 0; }
.doc-swatch { overflow: hidden; border: 1px solid var(--hali-border-default); border-radius: var(--hali-radius-lg); background: var(--hali-surface-raised); }
.doc-swatch__chip { height: 56px; border-bottom: 1px solid var(--hali-border-default); }
.doc-swatch__meta { display: flex; flex-direction: column; gap: 2px; padding: 8px 12px 10px; }
.doc-swatch__name { font: var(--hali-type-label-lg); }
.doc-swatch__var { color: var(--hali-text-subtle); font: var(--hali-type-code-md); font-size: 11px; word-break: break-all; }
.doc-swatch__vals { color: var(--hali-text-subtle); font: var(--hali-type-label-md); }
.doc-swatch__vals b { color: var(--hali-text-default); font-weight: 500; }

.doc-family {
  display: grid;
  gap: 8px;
  padding: 16px;
  border: 1px solid var(--hali-border-default);
  border-radius: var(--hali-radius-lg);
  background: var(--hali-surface-raised);
}
.doc-family__chips { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
/* accent.fill is a 3:1 graphics color, so a label never sits on it: the swatch is a block and the
   words sit on surface.strong, which is built for text. */
.doc-chip-key {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 28px;
  padding: 0 10px 0 8px;
  border-radius: var(--hali-radius-sm);
  background: var(--hali-surface-strong);
  color: var(--hali-text-default);
  font: var(--hali-type-label-md);
}
.doc-chip-key i { width: 14px; height: 14px; border-radius: 4px; flex: none; }
.doc-chip-bold, .doc-chip-container {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 10px;
  border-radius: var(--hali-radius-sm);
  font: var(--hali-type-label-md);
}
.doc-ratio { color: var(--hali-text-subtle); font: var(--hali-type-label-md); font-variant-numeric: tabular-nums; }

.doc-pair { display: grid; gap: 12px; grid-template-columns: 1fr 1fr; margin: 16px 0; }
.doc-pair > div { padding: 12px 16px; border: 1px solid var(--hali-border-default); border-radius: var(--hali-radius-lg); background: var(--hali-surface-raised); }
.doc-pair__do { border-top: 3px solid var(--hali-success-bold) !important; }
.doc-pair__dont { border-top: 3px solid var(--hali-danger-bold) !important; }
.doc-pair__tag { margin-bottom: 4px; font: var(--hali-type-label-md); }
.doc-pair__do .doc-pair__tag { color: var(--hali-success-text); }
.doc-pair__dont .doc-pair__tag { color: var(--hali-danger-text); }
@media (max-width: 599px) { .doc-pair { grid-template-columns: 1fr; } }

.doc-usage { display: grid; gap: 12px; grid-template-columns: 1fr 1fr; margin: 8px 0 16px; }
.doc-usage > div { padding: 12px 16px; border-radius: var(--hali-radius-lg); background: var(--hali-surface-raised); border: 1px solid var(--hali-border-default); }
.doc-usage h4 { margin-bottom: 6px; font: var(--hali-type-label-lg); }
.doc-usage ul { margin: 0; padding-left: 18px; color: var(--hali-text-default); }
.doc-usage li + li { margin-top: 4px; }
@media (max-width: 719px) { .doc-usage { grid-template-columns: 1fr; } }

.doc-table { margin: 16px 0; }
.doc-table .h-table td { vertical-align: top; }
.doc-sample { font-variant-numeric: normal; }

.doc-space-row { display: grid; grid-template-columns: 56px 56px minmax(0, 1fr); gap: 16px; align-items: center; padding: 6px 0; }
.doc-space-bar { height: 16px; border-radius: 2px; background: var(--hali-brand-bold); }

.doc-radius-grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); margin: 16px 0; }
.doc-radius { display: grid; gap: 8px; justify-items: start; }
.doc-radius__box { width: 96px; height: 64px; border: 2px solid var(--hali-brand-text); background: var(--hali-brand-container); }

.doc-ladder { display: grid; gap: 0; margin: 16px 0; border: 1px solid var(--hali-border-default); border-radius: var(--hali-radius-lg); overflow: hidden; }
.doc-ladder > div { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 16px; }
.doc-shadows { display: grid; gap: 24px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); padding: 32px 24px; border-radius: var(--hali-radius-lg); background: var(--hali-surface-default); border: 1px solid var(--hali-border-default); }
.doc-shadow-box { padding: 20px 16px; border-radius: var(--hali-radius-lg); background: var(--hali-surface-overlay); font: var(--hali-type-label-lg); }

.doc-bp { display: grid; gap: 8px; grid-template-columns: repeat(12, 1fr); margin: 16px 0; }
.doc-bp > div { height: 40px; border-radius: var(--hali-radius-sm); background: var(--hali-brand-container); color: var(--hali-brand-on-container); display: grid; place-items: center; font: var(--hali-type-label-md); }
.doc-shell-diagram { display: grid; grid-template-columns: 96px 1fr; grid-template-rows: 40px 160px; gap: 8px; margin: 16px 0; max-width: 560px; }
.doc-shell-diagram > div { display: grid; place-items: center; border-radius: var(--hali-radius-md); font: var(--hali-type-label-md); border: 1px dashed var(--hali-border-strong); }
.doc-shell-diagram__top { grid-column: 1 / -1; background: var(--hali-surface-raised); }
.doc-shell-diagram__side { background: var(--hali-surface-sunken); }
.doc-shell-diagram__main { background: var(--hali-surface-default); }

.doc-motion-row { display: grid; grid-template-columns: 140px minmax(0, 1fr) auto; gap: 16px; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--hali-border-default); }
.doc-motion-track { height: 32px; border-radius: var(--hali-radius-full); background: var(--hali-surface-sunken); position: relative; }
.doc-motion-dot { position: absolute; top: 4px; left: 4px; width: 24px; height: 24px; border-radius: 50%; background: var(--hali-brand-bold); transition-property: left; }
.doc-motion-dot.is-moved { left: calc(100% - 28px); }
@media (max-width: 599px) { .doc-motion-row { grid-template-columns: 1fr; } }

.doc-icons { display: grid; gap: 8px; grid-template-columns: repeat(auto-fill, minmax(104px, 1fr)); margin: 16px 0; }
.doc-icon {
  display: grid;
  gap: 8px;
  justify-items: center;
  padding: 16px 8px 10px;
  border: 1px solid var(--hali-border-default);
  border-radius: var(--hali-radius-lg);
  background: var(--hali-surface-raised);
  color: var(--hali-text-default);
  cursor: pointer;
}
.doc-icon:hover { background-image: linear-gradient(var(--hali-state-hover), var(--hali-state-hover)); border-color: var(--hali-border-strong); }
.doc-icon span { color: var(--hali-text-subtle); font: var(--hali-type-label-sm); text-align: center; word-break: break-word; }

.doc-chart { display: block; width: 100%; height: auto; }
.doc-chart text { fill: var(--hali-text-subtle); font: 500 11px/16px var(--hali-font-sans); }
.doc-legend { display: flex; flex-wrap: wrap; gap: 8px 16px; margin: 8px 0 0; padding: 0; list-style: none; font: var(--hali-type-label-md); }
.doc-legend li { display: inline-flex; align-items: center; gap: 6px; }
.doc-legend i { width: 10px; height: 10px; border-radius: 2px; }

.doc-type-row { display: grid; grid-template-columns: minmax(0, 1fr) 220px; gap: 16px; align-items: baseline; padding: 14px 0; border-bottom: 1px solid var(--hali-border-default); }
.doc-type-row code { color: var(--hali-text-subtle); }
@media (max-width: 719px) { .doc-type-row { grid-template-columns: 1fr; gap: 4px; } }

.doc-release { padding: 20px 0; border-bottom: 1px solid var(--hali-border-default); }
.doc-release h3 { display: flex; align-items: center; gap: 12px; font: var(--hali-type-title-lg); }
.doc-release h4 { margin: 16px 0 6px; font: var(--hali-type-label-lg); color: var(--hali-text-subtle); }
.doc-release ul { margin: 0; padding-left: 20px; max-width: 72ch; }
.doc-release li + li { margin-top: 6px; }

.doc-footer { margin-top: 96px; padding-top: 24px; border-top: 1px solid var(--hali-border-default); color: var(--hali-text-subtle); font: var(--hali-type-body-sm); }

@media (max-width: 839px) {
  .doc-layout { display: block; }
  .doc-nav { display: none; position: fixed; inset: 56px 0 0 0; z-index: var(--hali-z-overlay); height: auto; border-right: 0; }
  body.nav-open .doc-nav { display: block; }
  .doc-menu-btn { display: inline-grid; }
}
@media (max-width: 719px) {
  .doc-topbar .h-switch span { display: none; }
  .doc-topbar__tag { display: none; }
}
@media (max-width: 599px) {
  .doc-segmented-label { display: none; }
}
"""

DOC_JS = r"""
(function () {
  'use strict';
  var root = document.documentElement;

  function all(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function save(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  /* Theme and contrast */
  var theme = load('hali-docs-theme') === 'light' ? 'light' : 'dark';
  var more = load('hali-docs-contrast') === 'more';
  var palette = load('hali-docs-palette') || 'polar';
  function apply() {
    if (palette === 'polar') { root.removeAttribute('data-palette'); } else { root.setAttribute('data-palette', palette); }
    var ps = document.querySelector('[data-palette-select]');
    if (ps) { ps.value = palette; }
    root.setAttribute('data-theme', theme);
    if (more) { root.setAttribute('data-contrast', 'more'); } else { root.removeAttribute('data-contrast'); }
    all('[data-theme-set]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-theme-set') === theme ? 'true' : 'false');
    });
    var t = document.querySelector('[data-contrast-toggle]');
    if (t) { t.checked = more; }
  }
  all('[data-theme-set]').forEach(function (b) {
    b.addEventListener('click', function () { theme = b.getAttribute('data-theme-set'); save('hali-docs-theme', theme); apply(); });
  });
  var psel = document.querySelector('[data-palette-select]');
  if (psel) { psel.addEventListener('change', function () { palette = psel.value; save('hali-docs-palette', palette); apply(); }); }
  var ct = document.querySelector('[data-contrast-toggle]');
  if (ct) { ct.addEventListener('change', function () { more = ct.checked; save('hali-docs-contrast', more ? 'more' : 'normal'); apply(); }); }
  apply();

  /* Demo links should not jump the page */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('.doc-preview a[href^="#"], .doc-frame a[href^="#"], .doc-stage a[href^="#"]');
    if (a) { e.preventDefault(); }
  });

  /* Navigation filter */
  var filter = document.getElementById('nav-filter');
  var sections = all('.doc-nav__section');
  if (filter) {
    filter.addEventListener('input', function () {
      var q = filter.value.trim().toLowerCase();
      sections.forEach(function (s) {
        var any = false;
        all('a', s).forEach(function (a) {
          var show = !q || a.textContent.toLowerCase().indexOf(q) !== -1;
          a.hidden = !show;
          if (show) { any = true; }
        });
        s.hidden = !any;
      });
    });
  }

  /* Scroll spy */
  var links = all('.doc-nav a');
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) { return; }
        var a = byId[en.target.id];
        if (!a) { return; }
        links.forEach(function (l) { l.classList.remove('is-active'); l.removeAttribute('aria-current'); });
        a.classList.add('is-active');
        a.setAttribute('aria-current', 'location');
        try { a.scrollIntoView({ block: 'nearest' }); } catch (e) {}
      });
    }, { rootMargin: '-72px 0px -75% 0px' });
    all('[data-spy]').forEach(function (s) { io.observe(s); });
  }

  /* Mobile navigation */
  var menuBtn = document.querySelector('.doc-menu-btn');
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.forEach(function (a) { a.addEventListener('click', function () { document.body.classList.remove('nav-open'); menuBtn.setAttribute('aria-expanded', 'false'); }); });
  }

  /* Copy helpers */
  function copyText(text, done) {
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta);
      done();
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
  }
  all('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var code = btn.parentNode.querySelector('code');
      copyText(code ? code.textContent : '', function () {
        var old = btn.textContent; btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = old; }, 1400);
      });
    });
  });
  all('[data-snippet]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      copyText(btn.getAttribute('data-snippet'), function () {
        if (window.Hali) { window.Hali.toast('Copied ' + btn.getAttribute('data-name'), 'success', { duration: 2500 }); }
      });
    });
  });

  /* Token table filter */
  var tf = document.getElementById('token-filter');
  if (tf) {
    var rows = all('tr[data-token]');
    tf.addEventListener('input', function () {
      var q = tf.value.trim().toLowerCase();
      rows.forEach(function (r) { r.hidden = q && r.getAttribute('data-token').indexOf(q) === -1; });
    });
  }

  /* Motion demo */
  all('[data-motion]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var dot = btn.closest('.doc-motion-row').querySelector('.doc-motion-dot');
      dot.style.transitionDuration = btn.getAttribute('data-ms') + 'ms';
      dot.style.transitionTimingFunction = btn.getAttribute('data-ease');
      dot.classList.toggle('is-moved');
    });
  });
})();
"""
