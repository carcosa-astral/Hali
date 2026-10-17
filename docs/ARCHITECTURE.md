# Architecture

## How the pieces fit

```
scripts/build_tokens.py   Nord palette + rules  ->  tokens/hali-tokens.json
                                                ->  tokens/hali-tokens.css
                                                ->  tokens/CONTRAST.md
css/hali.css              reads only --hali-* custom properties from the tokens CSS
icons/hali-icons.svg      symbol sprite, styled by .h-icon
scripts/build_site.py     tokens JSON + CSS + icons + CHANGELOG  ->  site/index.html
```

Colors flow in one direction. The Python script is the only place a hex value is decided. The CSS never
contains a hard coded theme color, the site reads the generated JSON for its swatches and contrast
tables, and the contrast report is produced by the same code that picks the values.

## Token layers

1. **Raw Nord.** The sixteen Nord colors, exposed as `--hali-nord-0` to `--hali-nord-15`. Use these for
   illustration, syntax themes and brand art. Do not use them for UI text or fills.
2. **Semantic tokens.** The roles components use: `surface.*`, `text.*`, `icon.*`, `border.*`,
   `brand.*`, status (`danger.*`, `warning.*`, `success.*`, `info.*`, `discovery.*`), `accent.*`,
   `state.*`, `shadow.*`. These change per theme.
3. **Static tokens.** Type, space, radius, size, motion, breakpoints and layers. These do not change per
   theme.
4. **Component styles.** Classes in `css/hali.css` that consume semantic and static tokens, with a few
   private custom properties (`--_bg`, `--_fg`) for variants.

Build components from layer 2 and 3 only.

## Token naming

Path form in JSON: `<group>.<role>[.<state>]`, for example `text.subtle` or `brand.bold.hover`.
CSS form: the same path with dots turned into dashes and a `--hali-` prefix, for example
`--hali-text-subtle`.

| Group | Roles |
| --- | --- |
| `surface` | `sunken`, `default`, `raised`, `overlay`, `strong` |
| `text` | `default`, `subtle`, `subtlest`, `disabled`, `inverse` |
| `icon` | `default`, `subtle` |
| `border` | `default` (decorative), `strong` (3:1, use on fields), `focus` |
| `brand` | `bold`, `bold.hover`, `bold.pressed`, `on-bold`, `text`, `container`, `on-container` |
| `<status>` | `bold`, `on-bold`, `text`, `container` |
| `accent.<color>` | `fill`, `text`, `container` |
| `state` | `hover`, `pressed`, `scrim` |
| `shadow` | `raised`, `overlay`, `modal` |

### Bold, container and text

These three words come from Atlassian and Material and mean the same thing for every color family:

- **bold** is a solid fill. Pair it with its `on-bold` color for the label.
- **container** is a quiet tonal background. Pair it with the family's `text` color (or `on-container`
  for brand).
- **text** is the color to use for readable text or an icon of that family on a surface.

## Surfaces

Depth is tone. Five steps, from lowest to highest:

| Token | Use |
| --- | --- |
| `surface.sunken` | Inset wells, input backgrounds, code blocks |
| `surface.default` | The page canvas |
| `surface.raised` | Cards, panels, table containers |
| `surface.overlay` | Menus, popovers, dialogs, toasts |
| `surface.strong` | Hover and selected fills, neutral lozenges, default buttons |

In dark, higher steps are lighter. In light, `raised` and `overlay` are lighter than the page, and
`sunken` and `strong` are darker.

## Themes

The tokens CSS defines dark on `:root`, so with no attributes the page is dark. It switches to light only
when the system prefers light and no `data-theme` is set. Explicit `data-theme="dark"` or
`data-theme="light"` always wins. `data-contrast="more"` (or the system `prefers-contrast: more`) raises
secondary text, icons and decorative borders one step.

## Component conventions

- Blocks are `h-<name>`. Elements use `__`, modifiers use `--`.
- Variants that change color use a private `--_bg` and `--_fg` pair so state styles stay generic.
- Hover and pressed states use a Material style state layer: the label color at 8% and 14% opacity.
  Bold buttons use the dedicated `bold.hover` and `bold.pressed` tokens instead.
- Status color scopes (`h-is-success` and friends) set `--h-container`, `--h-text`, `--h-accent`,
  `--h-bold` and `--h-on-bold` once, and lozenges, alerts, banners, toasts, badges and progress bars all
  read them. Add a status to the system by adding a scope, not by adding per component rules.
- Native elements first: `button`, `a`, `input`, `select`, `dialog`, `details`, `table`.

## Layers

`css/hali.css` declares `@layer hali.base, hali.layout, hali.components, hali.utilities`. Your
unlayered CSS always beats Hali, so overriding a component never needs a specificity fight.
