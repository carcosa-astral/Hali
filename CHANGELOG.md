# Changelog

All notable changes to Hali are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). What counts as major, minor and patch for a
design language is spelled out in [docs/VERSIONING.md](docs/VERSIONING.md).

## [Unreleased]

## [3.0.0] - 2026-10-18

Hali stops looking like an enterprise console. Version 3 is soft where you touch and crisp where you read:
pill controls, borderless cards that get their depth from tone, a halo of brand light, deeper surfaces, and
two kinds of motion. It borrows structure from Atlassian, depth and state from Material 3, and layering,
contrast discipline and productive and expressive motion from IBM Carbon. Roles, class names and icons are
unchanged. Shape, size, type and the default palette are not, which is why this is a major release. See
[docs/MIGRATING-3.0.md](docs/MIGRATING-3.0.md).

### Breaking

- **Default palette is Polar, not Nord.** Roles and contrast guarantees hold. `data-palette="nord"` restores
  the 2.x palette.
- **`--hali-nord-*` is deprecated** and fixed to stock Nord. Use `--hali-palette-*`, which follows the active
  palette. In `tokens/hali-tokens.json` the `nord.*` keys inside themes are now `palette.*`.
- **Control heights grew:** `size-control-sm` 28 to 32, `-md` 36 to 40, `-lg` 44 to 48.
- **Shape:** buttons, chips, lozenges, segmented controls and navigation items are pills. Fields, alerts,
  toasts and menus are 18px. Cards, dialogs and table wrappers are 28px. Radius `xl` is 18.
- **Cards, dialogs, menus, toasts and table wrappers lost their border.** Use `h-card--outlined` for a line.
  `h-card` padding is 24 (was 16).
- **Type:** Inter and JetBrains Mono become IBM Plex Sans and IBM Plex Mono. Display and headlines move to
  Bricolage Grotesque at weight 700. `display` is 44/48 (was 40/48), `headline-lg` is 34/40 (was 32/40).
- **Segmented control:** the selected segment is a solid brand fill.
- **Toast:** no colored left bar.

### Added

- **Five palettes:** Polar (default), Aurora, Ember (its light theme is the sunrise one), Midnight (near
  black) and Nord (stock, opt in). Each has dark, light and increased contrast. Choose with `data-palette`.
- **`Hali.setPalette()`, `Hali.setTheme()` and `Hali.restore()`** in `js/hali.js`, with the choice remembered
  in the browser.
- **Shape roles:** `shape-control`, `shape-field`, `shape-card`, `shape-hero`, `shape-data`, and radius `3xl`.
- **Two kinds of motion.** Productive: `duration-productive` 160ms with `ease-productive` (from IBM Carbon's
  productive curve), for work. Expressive: `duration-expressive` 480ms with `ease-spring`, for wins and
  arrivals. Also `duration-micro` 70ms, `ease-productive-enter`, `ease-productive-exit`, `ease-expressive`.
- **Glow tokens:** `glow.brand` and `glow.soft`.
- **`type-hero`** (56/58) and `--hali-font-display`.
- **New components:** `h-hero` (with a ripple ring motif), `h-stat`, `h-bars`, `h-search`, `h-halo`,
  `h-sidenav--float` with `h-appshell--float`, and `h-lozenge--live`.
- `docs/BUILDING-WITH-HALI.md`: a working guide with setup, tokens, class cheat sheet, copy and paste patterns,
  icon use, voice rules and the list of known gaps.
- `docs/MIGRATING-3.0.md`.
- **Reference site:** a palette picker, a palette gallery, and pages for the new components.

### Changed

- Buttons lift 1px on hover and press to 97%. Bold buttons carry a soft brand glow. Fields show a glow ring
  on focus. Switch thumbs move with a small spring.
- Shadows are softer and larger. Light theme shadows are tinted with the palette's own deep color.
- Contrast checking now covers every palette in dark and light: 930 checks, all passing.
- Voice guidance allows a light touch in safe moments (success, empty states, first run).

## [2.1.0] - 2026-10-17

Icons. Hali gets 30 new icons with a ripple accent and a 16px set drawn for small controls. Nothing from
2.0 changes.

### Added

- **30 new icons** in `icons/hali-icons.svg`, filling the gaps a real app hit: `dollar`, `wallet`,
  `receipt`, `music`, `headphones`, `mic`, `volume`, `play`, `pause`, `users`, `user-plus`, `shield`,
  `key`, `tag`, `bookmark`, `map-pin`, `globe`, `image`, `share`, `undo`, `redo`, `grip`, `list`,
  `settings`, `heart`, `message`, `send`, `wifi`, `activity` and `trending-up`. The set is now 78 icons.
- **Ripple accent.** Each new icon draws one detail as a ripple arc, ring or dot, echoing the Hali mark.
  The detail uses `--hali-icon-accent`, which is the icon color by default, so every icon still works as
  a single color icon. Add `h-icon--duo` to color the accent with `brand.text`. The 1.0 icons are single
  color only.
- **16px icon set.** `icons/hali-icons-16.svg` holds 57 of the most used icons on a 16 grid, with ids
  `i16-<name>`. Use them with `h-icon--16` (1.5px stroke) in small controls, dense tables and text. The
  file is generated from the 24px drawings by `scripts/build_icons16.py`, which snaps strokes to the half
  pixel. Hand tuned replacements go in its `OVERRIDES`.
- `./icons-16.svg` export in `package.json`, a CI step that rebuilds the 16px set, and a version check
  for both sprites.
- **Reference site.** The Iconography page shows all 78 icons, the ripple accent, and the 16px set.

## [2.0.0] - 2026-10-17

The first release shaped by a real application. Designing the Deckhand club management app on Hali 1.0
showed what data heavy screens need: searchable and selectable tables, a bulk action bar, row density
that is a decision and not an accident, editing values in place, and clearer status and empty states.
The additions are listed from the Hali additions log kept during that work. Density is a layout metric
and the old class name is gone, which is why this is a major release. See
[docs/MIGRATING-2.0.md](docs/MIGRATING-2.0.md).

### Breaking

- **Removed `h-table--dense`.** Use `h-table--compact`. The compact row height is unchanged at 32px.
- **Table row height is now defined by tokens.** `--hali-size-row-default` (44px, the same height as
  before), `--hali-size-row-compact` (32px) and the new `--hali-size-row-comfortable` (56px). Overrides
  that set `padding-block` on `.h-table td` need to move to these tokens.

### Added

- **Data table tools.** Put `data-table-tools` on an `h-table-wrap` to get, with no JavaScript of your own:
  search that filters rows (`data-table-search`), a live row count (`data-table-count`), a no results
  slot (`data-table-empty`), a select all checkbox with a mixed state, row selection, a bulk action
  bar (`h-batchbar`) that replaces the toolbar while rows are selected, and a density switch
  (`data-density`). A `hali:selectionchange` event reports the selected rows.
- **Row density.** `h-table--compact`, the default, and `h-table--comfortable`.
- **Table extras.** `h-table--sticky` for a sticky header, `h-table__select` for the checkbox
  column, `h-table__empty` for an empty state that fills the table, `h-toolbar__count`.
- **Inline edit.** `h-inline-edit` with `data-inline-edit`: a value that turns into a field in place, with
  Save and Cancel, Enter and Escape, native validation, an optional suffix such as `%`, and a
  cancelable `hali:inline-save` event for saving to a server.
- **Lozenge dot and outline.** `h-lozenge .h-dot` for online, offline and degraded states, and
  `h-lozenge--outline` for quiet labels. Status is still carried by the word as well as the dot.
- **Compact empty state.** `h-empty--compact` for empty tables, cards and panels, with a documented
  first use pattern that offers one clear next action.
- **Reference site.** New or extended pages for Table, Inline edit, Lozenge and Empty state, each with
  live demos.

### Changed

- `.h-table td` vertical padding is computed from the row height tokens. Default and compact rows render at the
  same height as in 1.0.0.
- `js/hali.js` now covers table tools and inline edit. It is still optional and dependency free.

### Not changed

The header and side navigation shell, and status lozenges, were on the additions list and already
existed in 1.0.0. They are unchanged apart from the lozenge dot and outline above.

## [1.0.0] - 2026-10-17

First stable release. Hali is dark first: dark is the default theme, and light is derived from it.

### Added

- **Tokens.** Dark and light themes built from the Nord palette, plus an increased contrast layer.
  Surfaces (`sunken`, `default`, `raised`, `overlay`, `strong`), text, icon, border, brand, status
  (danger, warning, success, info, discovery), eight accent colors, state layers, scrim and shadows.
  Static tokens for type, space, radius, control and icon sizes, motion, breakpoints and layers.
  Delivered as `tokens/hali-tokens.json` and `tokens/hali-tokens.css`.
- **Readable Nord.** Stock Nord pairs that fail WCAG (comment gray at 1.7:1, most Aurora colors on
  light surfaces) are lifted in OKLCH so each hue keeps its character. All 186 checked pairings pass
  and are listed in `tokens/CONTRAST.md`.
- **Typography.** Fourteen roles that combine Material 3 naming (display, headline, title, body,
  label) with Atlassian density (14px default body).
- **Components.** Button (bold, tonal, outline, subtle, link, danger, sizes, icon only, loading, group),
  text input, textarea, select, checkbox, radio, switch, segmented control, field, label, help and
  error text, chip, lozenge, badge, dot, avatar and avatar group, card, alert, banner, toast, tabs,
  breadcrumbs, pagination, top bar, side navigation and rail, menu and dropdown, tooltip, dialog,
  side sheet, table with toolbar and sorting states, progress, spinner, skeleton, empty state,
  accordion, divider, keyboard key, code and code block, skip link.
- **Layout.** Container, stack, cluster, split, auto grid, 12 column grid on Material window size
  classes, app shell, page and page header.
- **Optional behavior.** `js/hali.js`, no dependencies, opt in through data attributes. Gives tabs
  (arrow, Home and End keys), dropdown menus (arrow keys, Escape, focus return), dialog open and close,
  chips, segmented controls, sortable tables and a `Hali.toast()` helper.
- **Icons.** 48 line icons on a 24px grid in `icons/hali-icons.svg`, and the Hali mark.
- **Accessibility.** Visible focus ring at 3:1 or better on every surface, 44px targets on coarse
  pointers, reduced motion handling, forced colors support, `prefers-contrast: more` support and a
  manual `data-contrast="more"` switch.
- **Documentation.** A single page reference site with foundations, components, patterns, content
  guidelines and resources, built by `scripts/build_site.py`.
- **Project.** README, versioning policy, architecture and accessibility notes, contributing guide,
  issue and pull request templates, and a CI workflow that rebuilds tokens and fails on any contrast or
  version mismatch.

### Known limitations

- No date picker, combobox, tree view, toast manager or chart components yet. Their absence is
  deliberate for 1.0 because each needs behavior that CSS alone cannot provide.
- Components are CSS first. Anything beyond what the optional `js/hali.js` provides, such as focus
  management inside custom widgets, is your application's job.
- Inter and JetBrains Mono are named in the font stacks but are not bundled. Without them the system
  fonts are used.

[Unreleased]: https://github.com/carcosa-astral/Hali/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/carcosa-astral/Hali/compare/v2.1.0...v3.0.0
[2.1.0]: https://github.com/carcosa-astral/Hali/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/carcosa-astral/Hali/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/carcosa-astral/Hali/releases/tag/v1.0.0
