# Versioning

Hali follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). The version is a single
number for the whole system. Tokens, CSS, icons and documentation always ship together, so there is
never a question of which token release matches which stylesheet.

The current version lives in the `VERSION` file. `package.json`, `tokens/hali-tokens.json`, the CSS
headers and the changelog must agree with it, and `scripts/check_version.py` enforces that.

## The public API

For a design language, the public API is everything a consumer can depend on:

- Token names and their meaning: `--hali-surface-raised` is a raised surface in every theme
- Token groups and the guarantees attached to them, such as "`text.subtle` is at least 6:1 on the core
  surfaces"
- CSS class names, modifiers and the HTML structure each component expects
- Icon ids in the sprite
- Layout metrics: control heights, spacing scale values, breakpoints, type scale sizes and line heights
- The theme switching attributes: `data-theme` and `data-contrast`
- Supported browsers

Specific color values are not part of the API. Roles and guarantees are. That is what lets Hali improve
a color without breaking anyone, as long as the roles and contrast guarantees hold.

## What changes the number

### Major (2.0.0)

Anything that requires a consumer to change their markup, CSS or layout:

- Removing or renaming a token, class, modifier or icon
- Changing the HTML structure a component requires
- Changing a layout metric: a control height, a spacing step, a breakpoint, a type size or line height
- Changing the meaning of a token, such as swapping what `brand.bold` is for
- Weakening a contrast guarantee
- Raising the minimum supported browser versions
- Changing the default theme

### Minor (1.1.0)

Backward compatible additions and refinements:

- New tokens, components, variants, modifiers or icons
- New themes or contrast layers
- Deprecating something, with a replacement in the same release
- Deliberate refinements of color values that keep every role and every contrast check passing. These
  are listed under **Changed** in the changelog so visual differences are never a surprise.

### Patch (1.0.1)

Fixes that do not change intent:

- Fixing a contrast miss or rendering bug
- Fixing a component state that did not behave as documented
- Documentation corrections and generated file regeneration
- Build script fixes that do not change output

A patch never adds API surface.

## Deprecation

1. Mark it in the release that introduces the replacement, under **Deprecated** in the changelog.
2. In CSS, add a comment: `/* @deprecated since 1.3.0, use .h-button--tonal */`. In the tokens JSON,
   add `"$deprecated": "since 1.3.0, use brand.container"` to the entry.
3. Keep it working for at least one full minor release.
4. Remove it only in the next major release, under **Removed**.

## Pre-releases

Pre-releases use SemVer suffixes: `1.1.0-beta.1`, `1.1.0-rc.1`. They are tagged and published like any
other release but are never the target of the `latest` reference. Pre-release APIs can change without a
major bump.

## Support policy

Only the latest major version receives fixes. When a new major ships, the previous major gets security
and accessibility fixes for six months, then ends.

## Release checklist

1. Move entries from **Unreleased** to a new dated section in `CHANGELOG.md`.
2. Update `VERSION` and `package.json`.
3. Update the version in the headers at the top of `css/hali.css` and `js/hali.js`, the `VERSION`
   constant in `js/hali.js`, and `VERSION` inside `scripts/build_tokens.py`.
4. Run `python3 scripts/build_tokens.py`. It must report zero failing checks.
5. Run `python3 scripts/build_site.py`.
6. Run `python3 scripts/check_version.py`. It must pass.
7. Commit: `chore(release): v1.1.0`.
8. Tag: `git tag -a v1.1.0 -m "Hali 1.1.0"` and push the tag.
9. Create a GitHub release from the tag and paste the changelog section.

## Changelog conventions

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Sections, in this
order: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**. Every entry says what
changed from a consumer's point of view, not which file was edited. Dates are `YYYY-MM-DD`.
