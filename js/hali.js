/*! Hali design language v1.0.0
 * Optional behavior for tabs, dropdowns, dialogs, chips, segmented controls, toasts and sortable tables.
 * No dependencies. Everything is opt in through data attributes.
 */
(function () {
  'use strict';

  var VERSION = '1.0.0';

  function all(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  /* ---- Dialogs: data-dialog-open="id", data-dialog-close ---------------------------------- */
  document.addEventListener('click', function (e) {
    var opener = e.target.closest('[data-dialog-open]');
    if (opener) {
      var dlg = document.getElementById(opener.getAttribute('data-dialog-open'));
      if (dlg && typeof dlg.showModal === 'function') { dlg.showModal(); }
      return;
    }
    var closer = e.target.closest('[data-dialog-close]');
    if (closer) {
      var parent = closer.closest('dialog');
      if (parent) { parent.close(); }
      return;
    }
    // A click on the backdrop lands on the dialog element itself, outside its box.
    if (e.target.tagName === 'DIALOG' && e.target.classList.contains('h-dialog')) {
      var r = e.target.getBoundingClientRect();
      var inside = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
      if (!inside) { e.target.close(); }
    }
  });

  /* ---- Tabs: data-tabs on a wrapper holding role=tablist and role=tabpanel ---------------- */
  function initTabs(root) {
    var tabs = all('[role="tab"]', root);
    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) { panel.hidden = !on; }
      });
      if (focus) { tab.focus(); }
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(tab, false); });
      tab.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowRight') { next = tabs[(i + 1) % tabs.length]; }
        else if (e.key === 'ArrowLeft') { next = tabs[(i - 1 + tabs.length) % tabs.length]; }
        else if (e.key === 'Home') { next = tabs[0]; }
        else if (e.key === 'End') { next = tabs[tabs.length - 1]; }
        if (next) { e.preventDefault(); select(next, true); }
      });
    });
  }
  all('[data-tabs]').forEach(initTabs);

  /* ---- Dropdown: data-dropdown, data-dropdown-toggle, a role=menu child ------------------- */
  all('[data-dropdown]').forEach(function (dd) {
    var btn = dd.querySelector('[data-dropdown-toggle]');
    var menu = dd.querySelector('[role="menu"]');
    if (!btn || !menu) { return; }

    function items() { return all('[role="menuitem"]:not(:disabled)', menu); }
    function open(focusFirst) {
      menu.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      if (focusFirst) { var list = items(); if (list[0]) { list[0].focus(); } }
    }
    function close(returnFocus) {
      menu.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
      if (returnFocus) { btn.focus(); }
    }

    btn.addEventListener('click', function () { if (menu.hidden) { open(false); } else { close(false); } });
    btn.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); open(true); }
    });
    menu.addEventListener('keydown', function (e) {
      var list = items();
      var i = list.indexOf(document.activeElement);
      if (!list.length) { return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); list[(i + 1) % list.length].focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); list[(i - 1 + list.length) % list.length].focus(); }
      else if (e.key === 'Home') { e.preventDefault(); list[0].focus(); }
      else if (e.key === 'End') { e.preventDefault(); list[list.length - 1].focus(); }
      else if (e.key === 'Escape') { e.preventDefault(); close(true); }
      else if (e.key === 'Tab') { close(false); }
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('[role="menuitem"]')) { close(true); }
    });
    document.addEventListener('click', function (e) {
      if (!dd.contains(e.target) && !menu.hidden) { close(false); }
    });
  });

  /* ---- Segmented control (single select) and chips (toggle) ------------------------------- */
  all('[data-segmented]').forEach(function (group) {
    group.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b || !group.contains(b)) { return; }
      all('button', group).forEach(function (x) {
        x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
      });
    });
  });
  all('[data-chips]').forEach(function (group) {
    group.addEventListener('click', function (e) {
      var chip = e.target.closest('.h-chip');
      if (!chip || !group.contains(chip)) { return; }
      chip.setAttribute('aria-pressed', chip.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
    });
  });

  /* ---- Toasts: Hali.toast(message, status) or data-toast="status|message" ---------------- */
  var TOAST_ICONS = { success: 'i-success', danger: 'i-error', warning: 'i-warning', info: 'i-info' };

  function toastRegion() {
    var region = document.querySelector('.h-toast-region');
    if (!region) {
      region = document.createElement('div');
      region.className = 'h-toast-region';
      document.body.appendChild(region);
    }
    return region;
  }

  function toast(message, status, options) {
    status = status || 'info';
    options = options || {};
    var duration = options.duration || 6000;
    var scope = status === 'info' ? 'brand' : status;

    var el = document.createElement('div');
    el.className = 'h-toast h-is-' + scope;
    el.setAttribute('role', status === 'danger' ? 'alert' : 'status');
    el.innerHTML =
      '<svg class="h-icon" aria-hidden="true"><use href="#' + (TOAST_ICONS[status] || 'i-info') + '"/></svg>' +
      '<span class="h-toast__message"></span>' +
      '<button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Dismiss">' +
      '<svg class="h-icon" aria-hidden="true"><use href="#i-close"/></svg></button>';
    el.querySelector('.h-toast__message').textContent = message;

    var timer = null;
    function dismiss() { clearTimeout(timer); if (el.parentNode) { el.parentNode.removeChild(el); } }
    function start() { timer = setTimeout(dismiss, duration); }
    function pause() { clearTimeout(timer); }

    el.querySelector('button').addEventListener('click', dismiss);
    el.addEventListener('mouseenter', pause);
    el.addEventListener('mouseleave', start);
    el.addEventListener('focusin', pause);
    el.addEventListener('focusout', start);

    toastRegion().appendChild(el);
    start();
    return { dismiss: dismiss };
  }

  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('[data-toast]');
    if (!trigger) { return; }
    var parts = trigger.getAttribute('data-toast').split('|');
    toast(parts.slice(1).join('|') || parts[0], parts.length > 1 ? parts[0] : 'info');
  });

  /* ---- Sortable tables: data-sortable on the table, buttons with .h-table__sort ----------- */
  all('[data-sortable]').forEach(function (table) {
    var body = table.tBodies[0];
    all('.h-table__sort', table).forEach(function (button) {
      button.addEventListener('click', function () {
        var th = button.closest('th');
        var index = th.cellIndex;
        var numeric = th.hasAttribute('data-numeric');
        var direction = th.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';

        all('th', table).forEach(function (other) { other.removeAttribute('aria-sort'); });
        th.setAttribute('aria-sort', direction);

        var rows = Array.prototype.slice.call(body.rows);
        rows.sort(function (a, b) {
          var x = a.cells[index].textContent.trim();
          var y = b.cells[index].textContent.trim();
          var result;
          if (numeric) {
            result = parseFloat(x.replace(/[^0-9.-]/g, '')) - parseFloat(y.replace(/[^0-9.-]/g, ''));
          } else {
            result = x.localeCompare(y);
          }
          return direction === 'ascending' ? result : -result;
        });
        rows.forEach(function (row) { body.appendChild(row); });
      });
    });
  });

  window.Hali = { version: VERSION, toast: toast };
})();
