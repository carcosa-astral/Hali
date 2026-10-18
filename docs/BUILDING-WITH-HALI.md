# Building with Hali

A working guide for anyone, or any AI assistant, building a web app on Hali. It is written to be read once and then used as a cheat sheet.

- Version this guide matches: **2.1.0**
- Source: https://github.com/carcosa-astral/Hali
- Full reference with live demos: open `site/index.html`

## The rules

1. **Dark first.** Dark is the default. Design in dark, check light.
2. **Never write a color.** Use a token: `var(--hali-surface-raised)`, never `#343B49`.
3. **Use the classes.** Names follow `h-block__element--modifier`. If a class does not exist, ask before inventing one.
4. **Status is never color alone.** Pair a status color with an icon and a word.
5. **Hali is styling only.** Do not put the Hali mark or name in a product. The site demos use the mark in a few examples. Replace it with your own logo.
6. **Readable always.** Primary text 7:1, secondary 6:1, anything readable 4.5:1, icons, borders and focus 3:1. Hali's tokens already meet this. Custom colors will not.
7. **Sentence case, verb first.** "Create project", not "Create Project" or "Submit".

## Setup

Copy `tokens/`, `css/`, `icons/` and `js/` into the project.

```html
<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <link rel="stylesheet" href="tokens/hali-tokens.css">
  <link rel="stylesheet" href="css/hali.css">
</head>
<body>
  <!-- paste icons/hali-icons.svg here once, and icons/hali-icons-16.svg if you use the 16px set -->
  <script src="js/hali.js" defer></script>
</body>
</html>
```

Load the tokens first. `js/hali.js` is optional. Without it the markup still renders, but tabs, menus, dialogs, toasts, table tools and inline edit do not act.

| To get | Set on `<html>` |
| --- | --- |
| Dark (default) | nothing, or `data-theme="dark"` |
| Light | `data-theme="light"` |
| Increased contrast | `data-contrast="more"` |

With no `data-theme`, Hali follows the system setting. Save the person's choice and set the attribute before the page paints so it does not flash.

## Tokens

All tokens are `--hali-<group>-<role>`. Every color token changes with the theme.

| Group | Tokens | Use for |
| --- | --- | --- |
| Surface | `surface-sunken`, `-default`, `-raised`, `-overlay`, `-strong` | Page canvas, page, cards and fields, menus and dialogs, hover and selection |
| Text | `text-default`, `-subtle`, `-subtlest`, `-disabled`, `-inverse` | Primary, secondary, hints, disabled, text on bold fills |
| Icon | `icon-default`, `-subtle` | Icons |
| Border | `border-default`, `-strong`, `-focus` | Dividers, input borders, focus ring |
| Brand | `brand-bold` (`-hover`, `-pressed`), `-on-bold`, `-text`, `-container`, `-on-container` | Primary button, links, selected states |
| Status | `danger`, `warning`, `success`, `info`, `discovery`, each with `-bold`, `-on-bold`, `-container`, `-text` | Alerts, lozenges, errors, banners |
| Accent | `accent-<teal, cyan, blue, red, orange, yellow, green, purple>` with `-container`, `-fill`, `-text` | Avatars, chips, chart series |
| State | `state-hover`, `state-pressed`, `state-scrim` | Hover and pressed layers, dialog backdrop |
| Shadow | `shadow-raised`, `-overlay`, `-modal` | Only things that float |

Static tokens (the same in every theme):

| Group | Tokens |
| --- | --- |
| Space | `space-2`, `4`, `6`, `8`, `12`, `16`, `20`, `24`, `32`, `40`, `48`, `64`, `80` |
| Radius | `radius-xs` 4, `sm` 6, `md` 8, `lg` 12, `xl` 16, `2xl` 28, `full` |
| Size | `size-control-sm` 28, `-md` 36, `-lg` 44, `size-icon-sm` 16, `-md` 20, `-lg` 24, `size-row-compact` 32, `-default` 44, `-comfortable` 56 |
| Type | `type-display`, `type-headline-lg/md/sm`, `type-title-lg/md/sm`, `type-body-lg/md/sm`, `type-label-lg/md/sm`, `type-code-md` |
| Motion | `duration-fast` 100ms, `-base` 200ms, `-slow` 300ms, `-deliberate` 500ms; `ease-standard`, `ease-enter`, `ease-exit` |
| Layers | `z-sticky`, `z-dropdown`, `z-overlay`, `z-modal`, `z-toast`, `z-tooltip` |

Breakpoints are Material window classes: compact under 600px, medium 600, expanded 840, large 1200, extra large 1600. Below 840px the side navigation hides and your app swaps it for a menu button and a sheet.

## Layout and type classes

| Need | Class |
| --- | --- |
| Page with a 1120px max width | `h-page` |
| Vertical stack with a gap | `h-stack h-gap-16` |
| Horizontal row that wraps | `h-cluster h-gap-8` |
| Space between two ends | `h-split` |
| Auto fit grid | `h-grid` with `style="--h-col:200px"` |
| 12 column grid | `h-columns` with `h-col-3`, `-4`, `-6`, `-8`, `-9`, `-full` |
| Push to the end | `h-spacer` |
| Type roles | `h-display`, `h-headline-lg/md/sm`, `h-title-lg/md/sm`, `h-body-lg/md/sm`, `h-label-lg/md/sm`, `h-code-md` |
| Numbers that line up | `h-tabular` |
| Surfaces | `h-surface-sunken`, `-default`, `-raised`, `-overlay`, `-strong` |
| Text colors | `h-text-default`, `-subtle`, `-subtlest`, `-brand`, `-danger`, `-warning`, `-success`, `-info`, `-discovery` |
| Screen reader only | `h-sr-only` |

Spacing helpers: `h-gap-0/4/8/12/16/24/32`, `h-mt-4/8/12/16/24/32`, `h-p-8/16/24`.

## Status and accent scopes

Put a scope class on any component and it takes that color: `h-is-brand`, `h-is-danger`, `h-is-warning`, `h-is-success`, `h-is-info`, `h-is-discovery`, `h-is-neutral`. For decoration use `h-accent-teal`, `-cyan`, `-blue`, `-red`, `-orange`, `-yellow`, `-green`, `-purple`.

```html
<span class="h-lozenge h-is-success"><span class="h-dot"></span>Online</span>
<div class="h-alert h-is-danger" role="alert">...</div>
```

Do not set `--h-container`, `--h-text` or `--h-bold` yourself. The scope classes set them.

## Components

Block names and their main parts. Every block has a demo, markup and guidance on the reference site.

| Group | Blocks |
| --- | --- |
| Actions | `h-button` (`--bold`, `--tonal`, `--outline`, `--subtle`, `--link`, `--danger`, `--danger-tonal`, `--sm`, `--lg`, `--icon`, `--block`), `h-button-group` |
| Forms | `h-field`, `h-label`, `h-help`, `h-error`, `h-input` (`--sm`, `--lg`), `h-textarea`, `h-select`, `h-input-group`, `h-fieldset`, `h-check`, `h-switch`, `h-segmented`, `h-chip`, `h-inline-edit` |
| Display | `h-lozenge` (`--bold`, `--outline`), `h-badge`, `h-dot`, `h-avatar` (`--sm`, `--lg`, `--xl`), `h-avatar-group`, `h-card` (`--elevated`, `--outlined`, `--interactive`), `h-accordion`, `h-divider`, `h-kbd`, `h-code`, `h-codeblock` |
| Feedback | `h-alert`, `h-banner`, `h-toast`, `h-progress`, `h-spinner`, `h-skeleton`, `h-empty` (`--compact`) |
| Navigation | `h-topbar`, `h-sidenav` (`--rail`), `h-tabs`, `h-breadcrumbs`, `h-pagination` |
| Overlays | `h-menu`, `h-dropdown`, `h-dialog` (`--sm`, `--lg`), `h-sheet` |
| Data | `h-table` (`--compact`, `--comfortable`, `--sticky`), `h-table-wrap`, `h-toolbar`, `h-batchbar` |
| Page | `h-appshell`, `h-page`, `h-page-header`, `h-section` |

## Patterns to copy

### Field

```html
<div class="h-field">
  <label class="h-label" for="name">Club name</label>
  <input class="h-input" id="name" type="text" aria-describedby="name-help">
  <div class="h-help" id="name-help">Shown on your public page.</div>
</div>
```

For an error, add `aria-invalid="true"` to the input and an `h-error` element with the message, linked with `aria-describedby`.

### Buttons

One bold button per view. Everything else steps down.

```html
<button class="h-button h-button--bold">Create event</button>
<button class="h-button h-button--outline">Export</button>
<button class="h-button h-button--subtle h-button--icon" aria-label="More"><svg class="h-icon" aria-hidden="true"><use href="#i-more"/></svg></button>
```

### Alert

```html
<div class="h-alert h-is-warning" role="status">
  <svg class="h-icon" aria-hidden="true"><use href="#i-warning"/></svg>
  <div>
    <div class="h-alert__title">Storage is almost full</div>
    <div class="h-alert__body">You have used 92% of your plan.</div>
  </div>
</div>
```

Use `role="alert"` only for urgent problems.

### Table with search, selection, bulk actions and density

```html
<div class="h-table-wrap" data-table-tools>
  <div class="h-toolbar">
    <div class="h-input-group" style="width:240px">
      <svg class="h-icon" aria-hidden="true"><use href="#i-search"/></svg>
      <input class="h-input h-input--sm" type="search" aria-label="Search people" data-table-search>
    </div>
    <span class="h-toolbar__count" data-table-count aria-live="polite"></span>
    <span class="h-spacer"></span>
    <button class="h-button h-button--bold h-button--sm">Invite people</button>
  </div>
  <div class="h-batchbar" data-batchbar hidden role="region" aria-label="Bulk actions">
    <span class="h-batchbar__count" data-batch-count aria-live="polite">0 selected</span>
    <button class="h-button h-button--tonal h-button--sm">Export</button>
    <span class="h-spacer"></span>
    <button class="h-button h-button--subtle h-button--sm" data-batch-clear>Clear selection</button>
  </div>
  <table class="h-table" data-sortable>
    <caption class="h-sr-only">People</caption>
    <thead><tr>
      <th scope="col" class="h-table__select"><label class="h-check"><input type="checkbox" data-select-all aria-label="Select all people"></label></th>
      <th scope="col">Name</th><th scope="col" data-numeric>Shifts</th>
    </tr></thead>
    <tbody>
      <tr><td class="h-table__select"><label class="h-check"><input type="checkbox" data-select-row aria-label="Select Ana Ruiz"></label></td><td>Ana Ruiz</td><td data-numeric>18</td></tr>
    </tbody>
  </table>
  <div class="h-empty h-empty--compact" data-table-empty hidden>
    <h3 class="h-empty__title">No one matches that search</h3>
  </div>
</div>
```

Density: add `h-table--compact` or `h-table--comfortable` to the table, or put `data-density="compact"` buttons inside the wrapper. Numbers get `data-numeric` and align right. Listen for `hali:selectionchange` on the wrapper to know which rows are selected.

### Inline edit

```html
<div class="h-inline-edit" data-inline-edit data-suffix="%">
  <button type="button" class="h-inline-edit__display" aria-label="Edit share of tips, currently 60%">
    <span class="h-inline-edit__value">60%</span>
    <svg class="h-icon" aria-hidden="true"><use href="#i-edit"/></svg>
  </button>
  <form class="h-inline-edit__form" hidden>
    <input class="h-input h-input--sm h-inline-edit__input" type="number" min="0" max="100" value="60" aria-label="Share of tips in percent" required>
    <button type="submit" class="h-button h-button--bold h-button--sm h-button--icon" aria-label="Save"><svg class="h-icon" aria-hidden="true"><use href="#i-check"/></svg></button>
    <button type="button" class="h-button h-button--subtle h-button--sm h-button--icon" aria-label="Cancel" data-inline-cancel><svg class="h-icon" aria-hidden="true"><use href="#i-close"/></svg></button>
  </form>
  <div class="h-inline-edit__error" role="alert" hidden></div>
</div>
```

To save to a server, listen for `hali:inline-save` on the wrapper. It carries `detail.value` and `detail.previous`. Call `event.preventDefault()` to stop Hali changing the text itself, then update it yourself when the server agrees.

### Confirm dialog

```html
<button class="h-button h-button--danger-tonal" data-dialog-open="dlg-delete">Delete club</button>
<dialog class="h-dialog h-dialog--sm" id="dlg-delete" aria-labelledby="dlg-delete-title">
  <div class="h-dialog__header"><h2 class="h-dialog__title" id="dlg-delete-title">Delete Vesper?</h2></div>
  <div class="h-dialog__body"><p>This removes the club and all of its events. It cannot be undone.</p></div>
  <div class="h-dialog__footer">
    <button class="h-button h-button--subtle" data-dialog-close>Cancel</button>
    <button class="h-button h-button--danger" data-dialog-close>Delete club</button>
  </div>
</dialog>
```

The button in the dialog repeats the title: "Delete Vesper?" and "Delete club". Never "OK" or "Yes".

### Toast

```html
<button class="h-button" data-toast="success|Event saved">Save</button>
```

Or from script: `Hali.toast('Event saved', 'success')`. Statuses are `success`, `info`, `warning` and `danger`.

### App shell

A top bar, a side navigation and a main area. Only the main area scrolls.

```html
<div class="h-appshell">
  <header class="h-appshell__top h-topbar">
    <a class="h-topbar__brand" href="/">YOUR LOGO</a>
    <div class="h-topbar__actions">...</div>
  </header>
  <nav class="h-appshell__side h-sidenav" aria-label="Main">
    <a class="h-sidenav__item" href="/" aria-current="page"><svg class="h-icon" aria-hidden="true"><use href="#i-home"/></svg> Dashboard</a>
    <div class="h-sidenav__section">Club</div>
    ...
  </nav>
  <main class="h-appshell__main">
    <div class="h-page">
      <div class="h-page-header">
        <div>
          <h1 class="h-page-header__title">Dashboard</h1>
          <p class="h-page-header__sub">One line that says what this page is for.</p>
        </div>
        <div class="h-page-header__actions">...</div>
      </div>
    </div>
  </main>
</div>
```

Every page gets a short intro line under its title. Every empty space gets an empty state with one clear next action.

## Icons

78 icons in `icons/hali-icons.svg` and 57 of them again in `icons/hali-icons-16.svg`.

```html
<svg class="h-icon" aria-hidden="true"><use href="#i-search"/></svg>
<svg class="h-icon h-icon--16" aria-hidden="true"><use href="#i16-search"/></svg>
```

Sizes: `h-icon--sm` 16px, default 20px, `h-icon--lg` 24px. Use the 16px set inside small controls and dense tables. Add `h-icon--duo` to the 30 icons added in 2.1.0 to color their ripple accent with the brand color.

Icon only buttons need `aria-label` on the button. Decorative icons get `aria-hidden="true"`.

To see every name, open the Iconography page on the reference site.

## Voice

Clear, calm, direct, human. No exclamation marks, no urgency theater, no jokes at the expense of a real problem.

| Situation | Write |
| --- | --- |
| Success | Project archived. |
| Warning | Storage is 92% full. Free up space or upgrade before uploads stop. |
| Error | We could not send the invite. Check the address and try again. |
| Destructive | This deletes 14 projects and cannot be undone. |
| Empty | No projects yet. Create one to get started. |

A product can layer its own brand voice over this for marketing pages. Inside the app UI, follow the table.

## What Hali does not have yet

If a screen needs one of these, build it from the existing blocks and tell the Hali maintainer so it can be added properly.

- Date picker, combobox, tree view, stepper and charts (planned after 2.x)
- KPI stat tile, simple bar chart, month calendar grid
- Page intro and inline field help as a documented pattern
- Ticket list with a reply thread, notification list, "viewing as" banner
- Knowledge base article layout, status board

The up to date list lives in the BACCHUS project file `hali-additions-log.md`.

## Keeping up with releases

Hali uses semantic versioning. A major version (2.0.0) means something you use was renamed or removed, and the changelog says what to change. A minor version (2.1.0) only adds. Read `CHANGELOG.md` before upgrading, and `docs/MIGRATING-2.0.md` if you are coming from 1.x.

The current release is 2.1.0.
