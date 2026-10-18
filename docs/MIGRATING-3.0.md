# Migrating from Hali 2.x to 3.0

Hali 3 changes how everything looks and feels. Class names, token names and icon ids stay, so most apps only
need to reload the CSS and tokens, add the fonts, and look at the screens. This page lists what changed so
nothing is a surprise.

## The 10 minute path

1. Replace `tokens/`, `css/`, `icons/` and `js/` with the 3.0 files.
2. Add the fonts (Google Fonts snippet below). Without them Hali falls back to system fonts.
3. Open each screen once. Check anything with a fixed height around a button or field (controls grew 4px).
4. If you want the old colors for now, add `data-palette="nord"` to `<html>`.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
```

## What breaks or shifts

### Color

- **The default palette is now Polar, not Nord.** Roles and contrast guarantees are the same, the values differ.
  `data-palette="nord"` gives the 2.x palette back, derived the same way.
- **`--hali-nord-0` to `--hali-nord-15` are deprecated.** They still exist and hold stock Nord values in every
  palette. The raw colors that follow the active palette are now `--hali-palette-0` to `--hali-palette-15`.
- **`tokens/hali-tokens.json`:** the `nord.*` keys inside each theme are now `palette.*`. A new `palettes`
  object holds every palette in dark and light. `theme` still holds the default palette.
- **Shadows are softer and larger.** Same three roles.
- **New tokens:** `glow.brand` and `glow.soft`.

### Shape and size

- **Controls grew:** `size-control-sm` 28 to 32, `-md` 36 to 40, `-lg` 44 to 48.
- **Radius `xl` is 18 (was 16).** New `3xl` is 32.
- **New shape roles:** `shape-control`, `shape-field`, `shape-card`, `shape-hero`, `shape-data`. Components use
  these. Retune a whole app by changing one role.
- **Pills:** buttons, chips, lozenges, segmented controls, top bar links and side navigation items.
- **Fields, alerts, toasts, menus:** 18px.
- **Cards, dialogs, table wrappers:** 28px.

### Borders

- **Cards, dialogs, menus, toasts and table wrappers no longer have a border.** Depth is tone. For the old
  look on a card add `h-card--outlined`.
- **`h-card` padding is 24 (was 16).** Use your own padding utility if you relied on 16.
- Fields, checkboxes, switches and chips keep their borders. A boundary must be visible at 3:1.

### Type

- **Fonts:** Inter becomes IBM Plex Sans, JetBrains Mono becomes IBM Plex Mono, and headlines use Bricolage
  Grotesque. New token `--hali-font-display`.
- **Display and headlines are bold (700) and in the display font.** `display` is 44/48 (was 40/48), `headline-lg`
  is 34/40 (was 32/40).
- **New role:** `type-hero` (56/58), class `h-type-hero`.

### Components

- **Segmented control:** the selected segment is now a solid brand fill (was a tonal container).
- **Toast:** no colored left bar. The icon and the words carry the status. It enters with a small spring.
- **Buttons** lift 1px on hover and press to 97%. Bold buttons carry a soft brand glow.
- **Lozenges** are pills and 24px tall.
- **Fields** show a soft glow ring while focused, on top of the focus outline.

### Motion

- New: `duration-micro` 70ms, `duration-productive` 160ms, `duration-expressive` 480ms.
- New easing: `ease-productive` (and `-enter`, `-exit`), `ease-expressive`, `ease-spring`.
- Old duration and easing names still work. Reduced motion still turns every duration to 0ms.

## What did not change

- Every token name and role, except the `nord.*` JSON keys above.
- Every class name. Nothing was renamed or removed.
- All 78 icons and 57 16px icons, and their ids.
- The theme attributes `data-theme` and `data-contrast`.
- Breakpoints, spacing scale, row heights.
- Supported browsers. The new styles use `color-mix()`, which every supported browser already has.

## New in 3.0

Five palettes (Polar, Aurora, Ember, Midnight, Nord), `Hali.setPalette()`, `Hali.setTheme()`, `Hali.restore()`,
`h-halo`, `h-hero`, `h-stat`, `h-bars`, `h-search`, `h-sidenav--float` with `h-appshell--float`, and
`h-lozenge--live`. See the changelog.
