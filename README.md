<p align="center">
  <img src="assets/hali-mark.svg" alt="Hali" width="72" height="72">
</p>

<h1 align="center">Hali</h1>

<p align="center">
  A dark first design language for web applications.<br>
  Nord at its core, Atlassian structure, Material 3 tonal surfaces, readable by default.
</p>

<p align="center">
  <strong>Version 2.0.0</strong> &nbsp;|&nbsp; <a href="CHANGELOG.md">Changelog</a> &nbsp;|&nbsp; <a href="docs/VERSIONING.md">Versioning</a> &nbsp;|&nbsp; <a href="docs/MIGRATING-2.0.md">Migrating to 2.0</a> &nbsp;|&nbsp; <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

## What Hali is

Hali is a small, complete system for building web apps that look calm and stay readable. It takes the
[Nord](https://www.nordtheme.com/) palette as its identity, borrows the semantic structure and density of
[Atlassian's design system](https://atlassian.design/), and borrows tonal surfaces, state layers, shape
and motion from [Material Design 3](https://m3.material.io/).

The name comes from Lake Hali: cold, still, and deep.

**Dark first.** Dark is the default theme and the one every decision is made in. Light is derived from
it, not the other way round. An increased contrast layer sits on top of both.

**Readable Nord.** Stock Nord is beautiful and a little too quiet. Its comment gray is 1.7:1 on its own
background, and most Aurora colors fail on light surfaces. Hali keeps the palette and lifts only what
fails, in OKLCH so every hue keeps its character. All 186 checked pairings meet their targets, and the
report is generated on every build: [tokens/CONTRAST.md](tokens/CONTRAST.md).

## Principles

1. **Dark first, light supported.** Design in dark. Derive light.
2. **Readable always.** 7:1 for primary text, 6:1 for secondary text, never below 4.5:1 for anything
   readable, 3:1 for icons, borders and focus.
3. **Calm density.** 14px body, a 4px grid, 36px controls. Quiet, not sparse.
4. **Tone over shadow.** Depth comes from tonal surface steps. Shadows are reserved for things that
   float.
5. **One source of truth.** Tokens are generated, checked and shipped as JSON and CSS. Nothing else
   hard codes a color.

## Quick start

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <link rel="stylesheet" href="tokens/hali-tokens.css">
  <link rel="stylesheet" href="css/hali.css">
</head>
<body>
  <button class="h-button h-button--bold">Create project</button>
  <script src="js/hali.js" defer></script> <!-- optional: tabs, menus, dialogs, toasts -->
</body>
</html>
```

Dark is the default. To choose a theme explicitly, set an attribute on the root element:

```html
<html data-theme="dark">     <!-- default -->
<html data-theme="light">
<html data-theme="light" data-contrast="more">
```

With no `data-theme`, Hali is dark, and switches to light only when the system asks for it with
`prefers-color-scheme: light`. `prefers-contrast: more` is honored automatically.

Use the icons by inlining `icons/hali-icons.svg` once per page, then reference a symbol:

```html
<svg class="h-icon" aria-hidden="true"><use href="#i-search"/></svg>
```

## What is inside

```
hali/
  tokens/        generated tokens: hali-tokens.json, hali-tokens.css, CONTRAST.md
  css/           hali.css: base, layout, typography, components, utilities
  js/            hali.js: optional behavior for tabs, menus, dialogs, toasts, table tools, inline edit
  icons/         hali-icons.svg: 24px line icon sprite
  assets/        the Hali mark
  site/          the generated reference site (open site/index.html)
  docs/          versioning, architecture and accessibility notes
  scripts/       build_tokens.py, build_site.py, check_version.py, hali_color.py
  CHANGELOG.md   release notes
  VERSION        the single source of the version number
```

## Foundations at a glance

| Foundation | Hali |
| --- | --- |
| Color | Nord Polar Night surfaces, Snow Storm text, Frost brand, Aurora status. Five tonal surface steps. |
| Type | Inter and JetBrains Mono. Fourteen roles on Material names, 14px default body. |
| Space | 4px grid. Tokens at 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80. |
| Shape | Controls 8px, cards 12px, dialogs 16px, pills for chips and badges. |
| Elevation | Tonal first, shadow only for menus, dialogs and toasts. |
| Motion | 100, 200, 300 and 500ms. Material easing curves. Honors reduced motion. |
| Layout | Material window size classes: 600, 840, 1200, 1600. 12 column grid. |
| Icons | 24px grid, 1.75px stroke, round caps. |

## Naming

| Thing | Pattern | Example |
| --- | --- | --- |
| Custom property | `--hali-<group>-<role>[-<state>]` | `--hali-surface-raised`, `--hali-brand-bold-hover` |
| Class | `h-<block>[__element][--modifier]` | `h-button--bold`, `h-card__title` |
| Scope helper | `h-is-<status>`, `h-accent-<color>` | `h-is-success` |
| Token path (JSON) | `<group>.<role>[.<state>]` | `text.subtle`, `brand.bold.hover` |

## Build

Requires Python 3.8 or newer. There are no dependencies.

```sh
python3 scripts/build_tokens.py   # tokens JSON, CSS and contrast report. Fails if any pairing misses.
python3 scripts/build_site.py     # the reference site in site/
python3 scripts/check_version.py  # version agrees everywhere
```

Never edit anything in `tokens/` by hand. Change `scripts/build_tokens.py` and rebuild.

## Browser support

Current evergreen browsers: Chrome and Edge 111 or newer, Safari 16.4 or newer, Firefox 113 or newer.
Hali uses cascade layers, `:has()`, `color-mix()` and CSS masks. Older browsers get a working but plainer
experience.

## Accessibility

Hali's targets and the checklist every component passes are in
[docs/ACCESSIBILITY.md](docs/ACCESSIBILITY.md). Components are CSS first, so correct markup and labels
are the application's job. The reference site shows the required markup for each component, and the
optional `js/hali.js` supplies the keyboard behavior for tabs, menus and dialogs.

## Project policy

- Versioning: [docs/VERSIONING.md](docs/VERSIONING.md)
- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Release notes: [CHANGELOG.md](CHANGELOG.md)

## Credits

The color palette is [Nord](https://www.nordtheme.com/) by Arctic Ice Studio. Hali's structure draws on
[Atlassian's design system](https://atlassian.design/) and [Material Design 3](https://m3.material.io/).
Hali is an independent project and is not affiliated with Atlassian, Google or Arctic Ice Studio.

## License

[MIT](LICENSE). The Nord palette is also MIT licensed, by Arctic Ice Studio. Inter and JetBrains Mono are
separate projects under the SIL Open Font License and are not bundled.
