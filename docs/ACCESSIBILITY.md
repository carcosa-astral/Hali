# Accessibility

Hali is designed to meet WCAG 2.2 level AA throughout, and AAA for primary text. This page states the
guarantees the system makes and the checklist a component must pass before it ships.

## Guarantees

| Area | Guarantee |
| --- | --- |
| Primary text | At least 7:1 on every surface, in both themes |
| Secondary text | At least 6:1 on the core surfaces (`sunken`, `default`, `raised`, `overlay`) |
| Tertiary text | At least 4.5:1 on the core surfaces |
| Status and accent text | At least 4.5:1 on the core surfaces and on its own container. On `surface.strong` at least 3:1, so pair it with an icon or a bold weight there |
| Brand text and links | At least 4.5:1 on every surface |
| Icons, field borders, focus ring | At least 3:1 against every adjacent surface |
| Focus | A 2px ring with a 2px offset on every interactive element, visible on every surface |
| Targets | 36px default controls. 44px on coarse pointers. Never below 24px |
| Motion | All transitions go to zero under `prefers-reduced-motion`. Spinners slow down but keep turning, because stopping them would hide a real state |
| Contrast preference | `prefers-contrast: more` and `data-contrast="more"` raise secondary text and decorative borders |
| Forced colors | Borders, selected states and the focus ring map to system colors |

Every pairing is checked at build time. Run `python3 scripts/build_tokens.py` and read
`tokens/CONTRAST.md`. The build fails if any pairing misses.

## Rules for using the system

- **Never convey meaning by color alone.** Status needs an icon or a word as well. Links inside
  running text keep their underline.
- **Do not put raw Nord colors on text.** Use semantic tokens. Raw Nord is for art.
- **Do not use `text.disabled` for anything someone needs to read.** It is exempt from contrast rules and
  intentionally quiet. Say why something is disabled in nearby help text.
- **Label every control.** A visible `h-label` linked with `for`/`id`, or `aria-label` for icon only
  buttons.
- **Keep one `h1` per page** and do not skip heading levels. Typography classes change how a heading
  looks, never what it is.

## Component checklist

A component is not done until each of these is true.

1. Built on a native element, or has the full ARIA pattern documented.
2. Fully usable by keyboard alone, with a visible focus state on every stop.
3. States designed and checked for contrast in both themes: default, hover, pressed, focus, disabled,
   selected, invalid, loading where they apply.
4. Name, role and value exposed to assistive technology.
5. Works at 200% zoom and 320px width without horizontal scrolling of the page.
6. Respects `prefers-reduced-motion`.
7. Has a forced colors treatment.
8. Meets the 44px target on coarse pointers.
9. Has a docs entry with required markup, and a changelog entry.

## Required markup by component

| Component | Must have |
| --- | --- |
| Icon only button | `aria-label`, and the icon `aria-hidden="true"` |
| Field | `label` with `for` matching the input `id`. Help and error text linked with `aria-describedby`. Invalid inputs set `aria-invalid="true"` |
| Checkbox, radio | A wrapping `label.h-check` |
| Switch | `role="switch"` on the checkbox input |
| Tabs | `role="tablist"`, `role="tab"` with `aria-selected`, `aria-controls`, and `role="tabpanel"` |
| Dialog | Native `<dialog>` opened with `showModal()`, labelled with `aria-labelledby` |
| Menu | `role="menu"` and `role="menuitem"`, arrow key navigation in your script |
| Toast | `role="status"` for information, `role="alert"` for errors, and enough time to read it |
| Table | `th` with `scope`, `caption` or `aria-label`, `aria-sort` on the sorted column |
| Progress | `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, or no value for indeterminate |
| Navigation | `nav` with an `aria-label`, and `aria-current="page"` on the current item |
| Skeleton | Wrapper has `aria-busy="true"` and a visually hidden "Loading" message |

## Testing

- Keyboard through every page without a mouse.
- Test with a screen reader: VoiceOver, NVDA or TalkBack.
- Switch the theme and the contrast mode, and turn on forced colors in your browser's developer tools.
- Turn on reduced motion and confirm nothing moves unnecessarily.
- Zoom to 200% and to 400%.
