# Migrating from Hali 1.x to 2.0

Two things break. Everything else in 1.x keeps working.

## 1. Rename `h-table--dense` to `h-table--compact`

```html
<!-- 1.x -->
<table class="h-table h-table--dense">

<!-- 2.0 -->
<table class="h-table h-table--compact">
```

Compact rows are 32px tall, the same as dense rows were. There is no alias, so a find and replace across
your templates is the whole migration.

## 2. Row height now comes from tokens

Table cell padding is now computed from three tokens:

| Token | Height | Class |
| --- | --- | --- |
| `--hali-size-row-compact` | 32px | `h-table--compact` |
| `--hali-size-row-default` | 44px | none |
| `--hali-size-row-comfortable` | 56px | `h-table--comfortable` |

Default and compact tables render at the same height as before. If your own CSS overrides
`padding-block` on `.h-table td`, change it to set the row token instead, or add a density class.

## What you can adopt

None of this is required, and none of it changes existing markup.

- Add `data-table-tools` to an `h-table-wrap` for search, selection, a bulk action bar and a density
  switch. See the Table page in the reference site for the markup.
- Use `h-inline-edit` for values that change in place.
- Use `h-lozenge .h-dot` for presence and health states, and `h-empty--compact` inside tables and cards.

Load the new `js/hali.js` to get the table tools and inline edit behavior. Without it, the markup still
renders and the controls simply do not act.
