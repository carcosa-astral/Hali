# Changelog

All notable changes to Hali are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). What counts as major, minor and patch for a
design language is spelled out in [docs/VERSIONING.md](docs/VERSIONING.md).

## [Unreleased]

### Added

- MIT `LICENSE` and `license` field in `package.json`.

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

[Unreleased]: https://github.com/carcosa-astral/Hali/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/carcosa-astral/Hali/releases/tag/v1.0.0
