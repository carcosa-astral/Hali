# Contributing to Hali

Thank you for helping. Hali is a small system and it stays useful by staying consistent, so most of this
page is about how to keep changes consistent.

## Ground rules

- Dark first. Design and review in dark, then check light and increased contrast.
- Readable always. A change that makes a pairing fail its contrast target does not merge.
- Tokens, not values. If you need a color, size or duration, it comes from a token. If no token fits,
  propose one.
- Native elements first. Reach for `button`, `dialog` and `details` before reaching for ARIA.

## Setup

Python 3.8 or newer. There are no dependencies.

```sh
git clone https://github.com/carcosa-astral/Hali.git
cd Hali
python3 scripts/build_tokens.py
python3 scripts/build_site.py
open site/index.html
```

## Making a change

| If you are changing | Do this |
| --- | --- |
| A color, status, accent or surface | Edit `scripts/build_tokens.py`, run it, and read the diff in `tokens/`. Commit the generated files. |
| A component | Edit `css/hali.css` and the matching entry in `scripts/site_content.py`. Show every state in the docs. |
| An icon | Add a `<symbol id="i-name">` to `icons/hali-icons.svg` on the 24px grid with a 1.75px stroke. The site picks it up automatically. |
| Behavior | Edit `js/hali.js`. Keep it dependency free, opt in through data attributes, and keep keyboard support complete. |
| Documentation | Edit the markdown in `docs/` or the content in `scripts/site_content.py`. |

Never edit files in `tokens/` or `site/` by hand. They are generated.

## Proposing a new component

Open an issue with the **Component request** template first. It should answer:

1. What job does it do that nothing in Hali does today?
2. Which native element or ARIA pattern does it build on?
3. What states does it have?
4. How does it behave at 320px, with a keyboard, and with a screen reader?

## Pull requests

- Branch from `main`: `feat/segmented-control`, `fix/switch-contrast`, `docs/tokens-page`.
- Use [Conventional Commits](https://www.conventionalcommits.org/): `feat(button): add tonal variant`,
  `fix(table): keep header sticky in compact mode`, `docs: clarify surface roles`.
- Add an entry under **Unreleased** in `CHANGELOG.md`. Say what changed from a consumer's point of view.
- Run `python3 scripts/build_tokens.py` (zero failing checks) and `python3 scripts/check_version.py`.
- Fill in the pull request template. It includes the accessibility checklist from
  [docs/ACCESSIBILITY.md](docs/ACCESSIBILITY.md).

## Versioning

Read [docs/VERSIONING.md](docs/VERSIONING.md) before changing a class name, token name, layout metric
or HTML structure. Those are breaking changes and wait for a major release.

## Writing style

Docs and UI copy follow the content guidelines on the reference site: plain, specific and short.
Sentence case for headings and buttons. No exclamation marks. No em dashes.
