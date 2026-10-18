#!/usr/bin/env python3
"""Build the Hali design tokens.

Reads the stock Nord palette, derives readable dark and light themes from it (dark is the
primary theme), verifies every text and UI pairing against WCAG, and writes:

    tokens/hali-tokens.json   machine readable source of truth
    tokens/hali-tokens.css    CSS custom properties (dark default, light, increased contrast)
    tokens/CONTRAST.md        generated contrast report

Run from the repository root:

    python3 scripts/build_tokens.py

The script exits with a non-zero status if any required pairing misses its target.
"""

import json
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hali_color import BLACK, WHITE, contrast, ensure, hex2rgb, mix, rgba, shift_l, soften  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "tokens")

VERSION = "3.0.0"

# ---------------------------------------------------------------------------------------------
# Palettes. Every palette fills the same sixteen slots, so one engine builds all of them:
#   0-3   deep ramp: 0 page (dark), 1 overlay, 2 strong, 3 border
#   4-6   light ramp: 4 strong (light), 5 sunken (light), 6 page (light) and text on dark
#   7-10  brand family: 7 teal, 8 brand on dark, 9 blue, 10 brand on light
#   11-15 signals: red, orange, yellow, green, purple
# Keys are kept as nord0..nord15 so the engine below reads like it always has.
# ---------------------------------------------------------------------------------------------
def _ramp(*values):
    return {"nord%d" % i: v for i, v in enumerate(values)}


NORD = _ramp(  # stock Nord (https://www.nordtheme.com/docs/colors-and-palettes), kept as an opt-in
    "#2E3440", "#3B4252", "#434C5E", "#4C566A", "#D8DEE9", "#E5E9F0", "#ECEFF4",
    "#8FBCBB", "#88C0D0", "#81A1C1", "#5E81AC", "#BF616A", "#D08770", "#EBCB8B", "#A3BE8C", "#B48EAD")

POLAR = _ramp(  # ink navy, glacier cyan, aurora signals
    "#111827", "#1F2A4D", "#2B3961", "#33425F", "#D6E0F0", "#E4EBF6", "#F1F5FB",
    "#7EE2D0", "#6CD4F0", "#7FA6F5", "#1F7FA8", "#F58A80", "#F5A06B", "#F5C96B", "#7EE2B8", "#B3A4FF")

AURORA = _ramp(  # deep violet night, soft lilac brand
    "#151128", "#251F48", "#352C5E", "#3B3260", "#DAD2F0", "#E9E4F7", "#F4F1FC",
    "#86EBC0", "#B9A6FF", "#8FA8FF", "#5A3FD6", "#F58E9E", "#F5A87C", "#F5CB78", "#86EBC0", "#D2A8F5")

EMBER = _ramp(  # warm wine-brown dark with an apricot brand; the light theme is the sunrise one
    "#1E1315", "#342022", "#4A3033", "#553A3C", "#F1DCCB", "#F7E9DC", "#FFF5EC",
    "#7FD6C2", "#F8A57A", "#8FA8E8", "#C2410C", "#F2756B", "#F7B267", "#F6D06F", "#8FDDAA", "#C7A6F2")

MIDNIGHT = _ramp(  # near black for late nights and OLED, moon blue brand
    "#07090F", "#151B31", "#1E2742", "#2A3452", "#CBD5EA", "#E2E8F5", "#EEF3FC",
    "#7FD6E0", "#8AB4FF", "#6C8CF0", "#2F55C8", "#F58A9A", "#F5A06B", "#F2CF7A", "#7EE2B8", "#C0A0FF")

# name: (label, note, colors, light_from). light_from reuses another palette's light theme.
PALETTES = {
    "polar": ("Polar", "The default. Ink navy surfaces, glacier cyan brand, aurora signals.", POLAR, None),
    "aurora": ("Aurora", "Deep violet night with a lilac brand.", AURORA, None),
    "ember": ("Ember", "Warm wine-brown and apricot in dark. The light theme is the sunrise one.", EMBER, None),
    "midnight": ("Midnight", "The darkest. Near black surfaces for late nights and OLED. Light uses Polar.", MIDNIGHT, "polar"),
    "nord": ("Nord", "Stock Nord, kept for apps that want the 2.x look.", NORD, None),
}
DEFAULT_PALETTE = "polar"


def status_raw(N):
    return {
        "danger": N["nord11"],
        "warning": N["nord13"],
        "success": N["nord14"],
        "info": N["nord10"] if N is NORD else N["nord9"],
        "discovery": N["nord15"],
    }


def accent_raw(N):
    return {
        "teal": N["nord7"],
        "cyan": N["nord8"],
        "blue": N["nord9"] if N is not NORD else N["nord10"],
        "red": N["nord11"],
        "orange": N["nord12"],
        "yellow": N["nord13"],
        "green": N["nord14"],
        "purple": N["nord15"],
    }


SURFACE_ORDER = ["sunken", "default", "raised", "overlay", "strong"]

# Contrast targets
AAA = 7.0        # primary text
SECONDARY = 6.0  # secondary text
AA = 4.5         # minimum for all readable text
UI = 3.0         # icons, borders, focus rings, large text


def build_theme(mode, N):
    """Return (tokens, checks, increased-contrast overrides) for 'dark' or 'light'.

    checks is a list of (label, foreground, background, minimum) tuples.
    """
    dark = mode == "dark"
    direction = 1 if dark else -1  # which way colors move to gain contrast
    t = {}
    checks = []

    # ---- Surfaces: Atlassian names, Material style tonal steps --------------------------------
    if dark:
        t["surface.sunken"] = mix(N["nord0"], BLACK, 0.14)
        t["surface.default"] = N["nord0"]
        t["surface.raised"] = mix(N["nord0"], N["nord1"], 0.5)
        t["surface.overlay"] = N["nord1"]
        t["surface.strong"] = N["nord2"]
    else:
        t["surface.sunken"] = N["nord5"]
        t["surface.default"] = N["nord6"]
        t["surface.raised"] = mix(N["nord6"], WHITE, 0.6)
        t["surface.overlay"] = mix(N["nord6"], WHITE, 0.85)
        t["surface.strong"] = N["nord4"]

    surfaces = [t["surface." + n] for n in SURFACE_ORDER]
    core = surfaces[:4]  # every surface except the strong hover and selected fill
    strong = t["surface.strong"]
    base = t["surface.default"]

    # ---- Text -------------------------------------------------------------------------------
    if dark:
        t["text.default"] = N["nord6"]
        t["text.subtle"] = soften(N["nord6"], N["nord3"], core, SECONDARY)
        t["text.subtlest"] = soften(N["nord4"], N["nord3"], core, AA)
        t["text.disabled"] = soften(N["nord4"], N["nord3"], [base], 2.6)
        t["text.inverse"] = N["nord0"]
    else:
        t["text.default"] = N["nord0"]
        t["text.subtle"] = soften(N["nord0"], N["nord6"], core, SECONDARY)
        t["text.subtlest"] = soften(N["nord0"], N["nord6"], core, AA)
        t["text.disabled"] = soften(N["nord0"], N["nord6"], [base], 2.6)
        t["text.inverse"] = N["nord6"]

    t["icon.default"] = t["text.subtle"]
    t["icon.subtle"] = t["text.subtlest"]

    for i, s in enumerate(SURFACE_ORDER):
        checks.append(("text.default on surface.%s" % s, t["text.default"], t["surface." + s], AAA))
    for s in SURFACE_ORDER[:4]:
        checks.append(("text.subtle on surface.%s" % s, t["text.subtle"], t["surface." + s], SECONDARY))
        checks.append(("text.subtlest on surface.%s" % s, t["text.subtlest"], t["surface." + s], AA))
    checks.append(("text.subtle on surface.strong", t["text.subtle"], strong, AA))
    checks.append(("text.subtlest on surface.strong", t["text.subtlest"], strong, UI))

    # ---- Borders ----------------------------------------------------------------------------
    if dark:
        t["border.default"] = N["nord3"]
        t["border.strong"] = soften(N["nord4"], N["nord0"], core, UI)
    else:
        t["border.default"] = mix(N["nord4"], N["nord3"], 0.15)
        t["border.strong"] = soften(N["nord3"], N["nord6"], core, UI)
    for s in SURFACE_ORDER[:4]:
        checks.append(("border.strong on surface.%s" % s, t["border.strong"], t["surface." + s], UI))

    # ---- Brand (Frost) ----------------------------------------------------------------------
    if dark:
        t["brand.on-bold"] = N["nord0"]
        t["brand.bold"] = shift_l(N["nord8"], direction, [t["brand.on-bold"]], AA)
        t["brand.bold.hover"] = mix(t["brand.bold"], WHITE, 0.12)
        t["brand.bold.pressed"] = mix(t["brand.bold"], N["nord0"], 0.14)
        t["brand.text"] = shift_l(N["nord8"], direction, surfaces, AA)
        t["brand.container"] = mix(base, N["nord8"], 0.20)
        t["brand.on-container"] = ensure(
            mix(N["nord6"], N["nord8"], 0.25), N["nord6"], [t["brand.container"]], AAA)
    else:
        t["brand.on-bold"] = N["nord6"]
        t["brand.bold"] = shift_l(N["nord10"], direction, [t["brand.on-bold"]], AA)
        t["brand.bold.hover"] = mix(t["brand.bold"], N["nord0"], 0.12)
        t["brand.bold.pressed"] = mix(t["brand.bold"], N["nord0"], 0.24)
        t["brand.text"] = shift_l(N["nord10"], direction, surfaces, AA)
        t["brand.container"] = mix(base, N["nord8"], 0.30)
        t["brand.on-container"] = ensure(
            mix(N["nord0"], N["nord10"], 0.30), N["nord0"], [t["brand.container"]], AAA)

    for s in SURFACE_ORDER:
        checks.append(("brand.text on surface.%s" % s, t["brand.text"], t["surface." + s], AA))
    for k in ("brand.bold", "brand.bold.hover", "brand.bold.pressed"):
        checks.append(("brand.on-bold on %s" % k, t["brand.on-bold"], t[k], AA))
    checks.append(("brand.on-container on brand.container", t["brand.on-container"], t["brand.container"], AAA))
    checks.append(("brand.bold on surface.default (fill edge)", t["brand.bold"], base, UI))

    # Focus ring (non-text, 3:1 on every surface)
    t["border.focus"] = shift_l(t["brand.bold"], direction, surfaces, UI)
    for s in SURFACE_ORDER:
        checks.append(("border.focus on surface.%s" % s, t["border.focus"], t["surface." + s], UI))

    # ---- Status (Aurora) --------------------------------------------------------------------
    for name, raw in status_raw(N).items():
        container = mix(base, raw, 0.15 if dark else 0.16)
        t["%s.container" % name] = container
        text_bgs = core + [container]
        if dark:
            t["%s.on-bold" % name] = N["nord0"]
            t["%s.bold" % name] = shift_l(raw, direction, [N["nord0"]], AA)
        elif name == "warning":
            t["%s.on-bold" % name] = N["nord0"]
            t["%s.bold" % name] = shift_l(raw, 1, [N["nord0"]], AA)
        else:
            t["%s.on-bold" % name] = N["nord6"]
            t["%s.bold" % name] = shift_l(raw, direction, [N["nord6"]], AA)
        t["%s.text" % name] = shift_l(raw, direction, text_bgs, AA)
        for s in SURFACE_ORDER[:4]:
            checks.append(("%s.text on surface.%s" % (name, s), t["%s.text" % name], t["surface." + s], AA))
        checks.append(("%s.text on surface.strong" % name, t["%s.text" % name], strong, UI))
        checks.append(("%s.text on %s.container" % (name, name), t["%s.text" % name], container, AA))
        checks.append(("%s.on-bold on %s.bold" % (name, name), t["%s.on-bold" % name], t["%s.bold" % name], AA))

    # ---- Accents (labels, avatars, chart marks) ---------------------------------------------
    for name, raw in accent_raw(N).items():
        container = mix(base, raw, 0.15 if dark else 0.16)
        t["accent.%s.container" % name] = container
        text_bgs = core + [container]
        t["accent.%s.fill" % name] = shift_l(raw, direction, core, UI)
        t["accent.%s.text" % name] = shift_l(raw, direction, text_bgs, AA)
        checks.append(("accent.%s.text on accent.%s.container" % (name, name),
                       t["accent.%s.text" % name], container, AA))
        checks.append(("accent.%s.text on surface.default" % name,
                       t["accent.%s.text" % name], base, AA))
        checks.append(("accent.%s.fill on surface.default" % name,
                       t["accent.%s.fill" % name], base, UI))

    # ---- State layers, scrim, shadows, glow --------------------------------------------------
    n0 = N["nord0"]
    if dark:
        t["state.hover"] = rgba(N["nord6"], 0.08)
        t["state.pressed"] = rgba(N["nord6"], 0.14)
        t["state.scrim"] = rgba(mix(n0, BLACK, 0.55), 0.66)
        t["shadow.raised"] = "0 1px 2px rgba(0, 0, 0, 0.28), 0 8px 24px -10px rgba(0, 0, 0, 0.50)"
        t["shadow.overlay"] = "0 6px 16px rgba(0, 0, 0, 0.34), 0 18px 40px -12px rgba(0, 0, 0, 0.50)"
        t["shadow.modal"] = "0 16px 40px rgba(0, 0, 0, 0.46), 0 32px 72px -16px rgba(0, 0, 0, 0.55)"
        t["glow.brand"] = rgba(t["brand.bold"], 0.38)
        t["glow.soft"] = rgba(t["brand.bold"], 0.14)
    else:
        sh = hex2rgb(n0)
        t["state.hover"] = rgba(n0, 0.07)
        t["state.pressed"] = rgba(n0, 0.12)
        t["state.scrim"] = rgba(n0, 0.45)
        t["shadow.raised"] = "0 1px 2px rgba(%d, %d, %d, 0.10), 0 8px 24px -12px rgba(%d, %d, %d, 0.22)" % (sh + sh)
        t["shadow.overlay"] = "0 6px 16px rgba(%d, %d, %d, 0.12), 0 18px 40px -14px rgba(%d, %d, %d, 0.26)" % (sh + sh)
        t["shadow.modal"] = "0 16px 40px rgba(%d, %d, %d, 0.18), 0 32px 72px -18px rgba(%d, %d, %d, 0.30)" % (sh + sh)
        t["glow.brand"] = rgba(t["brand.bold"], 0.30)
        t["glow.soft"] = rgba(t["brand.bold"], 0.10)

    # ---- Raw palette (for charts, syntax themes, brand art) --------------------------
    for k, v in N.items():
        t["palette.%s" % k[4:]] = v

    # ---- Increased contrast overrides ------------------------------------------------------
    more = {
        "text.subtle": t["text.default"],
        "text.subtlest": t["text.subtle"],
        "border.default": t["border.strong"],
        "icon.default": t["text.default"],
        "icon.subtle": t["text.subtle"],
    }

    return t, checks, more


STATIC = {
    "font": {
        "display": '"Bricolage Grotesque", "IBM Plex Sans", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
        "sans": '"IBM Plex Sans", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        "mono": '"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace',
    },
    # role: (family, weight, size px, line height px, tracking em)
    "type": {
        "hero": ("display", 700, 56, 58, -0.025),
        "display": ("display", 700, 44, 48, -0.02),
        "headline-lg": ("display", 700, 34, 40, -0.02),
        "headline-md": ("display", 700, 28, 36, -0.015),
        "headline-sm": ("display", 700, 24, 32, -0.01),
        "title-lg": ("sans", 600, 20, 28, 0),
        "title-md": ("sans", 600, 16, 24, 0),
        "title-sm": ("sans", 600, 14, 20, 0),
        "body-lg": ("sans", 400, 16, 24, 0),
        "body-md": ("sans", 400, 14, 20, 0),
        "body-sm": ("sans", 400, 12, 16, 0.005),
        "label-lg": ("sans", 500, 14, 20, 0.005),
        "label-md": ("sans", 500, 12, 16, 0.01),
        "label-sm": ("sans", 500, 11, 16, 0.02),
        "code-md": ("mono", 400, 13, 20, 0),
    },
    "space": [2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80],
    "radius": {"xs": 4, "sm": 6, "md": 8, "lg": 12, "xl": 18, "2xl": 28, "3xl": 32, "full": 9999},
    # Soft where you touch, crisp where you read. Components use these roles, not the scale.
    "shape": {"data": "md", "field": "xl", "card": "2xl", "hero": "3xl", "control": "full"},
    "size": {
        "control-sm": 32, "control-md": 40, "control-lg": 48,
        "row-compact": 32, "row-default": 44, "row-comfortable": 56,
        "icon-sm": 16, "icon-md": 20, "icon-lg": 24,
    },
    "motion": {
        # fast, base, slow, deliberate are the 2.x names and still work.
        # productive is for work (tables, menus, filters). expressive is for wins and arrivals.
        "duration": {"micro": 70, "fast": 100, "productive": 160, "base": 200, "slow": 300,
                     "expressive": 480, "deliberate": 500},
        "easing": {
            "standard": "cubic-bezier(0.2, 0, 0, 1)",
            "enter": "cubic-bezier(0.05, 0.7, 0.1, 1)",
            "exit": "cubic-bezier(0.3, 0, 0.8, 0.15)",
            "productive": "cubic-bezier(0.2, 0, 0.38, 0.9)",
            "productive-enter": "cubic-bezier(0, 0, 0.38, 0.9)",
            "productive-exit": "cubic-bezier(0.2, 0, 1, 0.9)",
            "expressive": "cubic-bezier(0.4, 0.14, 0.3, 1)",
            "spring": "cubic-bezier(0.34, 1.56, 0.64, 1)",
        },
    },
    "breakpoint": {"compact": 0, "medium": 600, "expanded": 840, "large": 1200, "xlarge": 1600},
    "z": {"sticky": 200, "dropdown": 400, "overlay": 500, "modal": 600, "toast": 700, "tooltip": 800},
    "focus": {"width": 2, "offset": 2},
}


def css_name(dotted):
    return "--hali-" + dotted.replace(".", "-")


def block(selector, tokens):
    lines = ["%s {" % selector]
    for k, v in tokens.items():
        lines.append("  %s: %s;" % (css_name(k), v))
    lines.append("}")
    return "\n".join(lines)


def static_css():
    out = {}
    out["--hali-font-display"] = STATIC["font"]["display"]
    out["--hali-font-sans"] = STATIC["font"]["sans"]
    out["--hali-font-mono"] = STATIC["font"]["mono"]
    for role, (fam, weight, size, line, track) in STATIC["type"].items():
        out["--hali-type-%s" % role] = "%d %dpx/%dpx var(--hali-font-%s)" % (weight, size, line, fam)
        out["--hali-tracking-%s" % role] = "%gem" % track
    for n in STATIC["space"]:
        out["--hali-space-%d" % n] = "%dpx" % n
    for k, v in STATIC["radius"].items():
        out["--hali-radius-%s" % k] = "%dpx" % v
    for role, step in STATIC["shape"].items():
        out["--hali-shape-%s" % role] = "var(--hali-radius-%s)" % step
    for i, (k, v) in enumerate(NORD.items()):  # deprecated in 3.0: stock Nord, same values as 2.x
        out["--hali-nord-%d" % i] = v
    for k, v in STATIC["size"].items():
        out["--hali-size-%s" % k] = "%dpx" % v
    for k, v in STATIC["motion"]["duration"].items():
        out["--hali-duration-%s" % k] = "%dms" % v
    for k, v in STATIC["motion"]["easing"].items():
        out["--hali-ease-%s" % k] = v
    for k, v in STATIC["z"].items():
        out["--hali-z-%s" % k] = str(v)
    out["--hali-focus-width"] = "%dpx" % STATIC["focus"]["width"]
    out["--hali-focus-offset"] = "%dpx" % STATIC["focus"]["offset"]
    lines = [":root {"]
    for k, v in out.items():
        lines.append("  %s: %s;" % (k, v))
    lines.append("}")
    return "\n".join(lines)


def nest(text, spaces=2):
    return textwrap.indent(text, " " * spaces)


def palette_css(name, dark, light, dark_more, light_more):
    """CSS for one palette. The default palette answers to a bare :root, the others to data-palette."""
    pre = "" if name == DEFAULT_PALETTE else '[data-palette="%s"]' % name
    bare = ":root,\n" if name == DEFAULT_PALETTE else ""
    dark_sel = '%s:root%s,\n:root%s[data-theme="dark"]' % (bare, pre, pre) if pre else ':root,\n:root[data-theme="dark"]'
    parts = [
        "/* %s */" % PALETTES[name][0],
        block(dark_sel, dark),
        "@media (prefers-color-scheme: light) {",
        nest(block(':root%s:not([data-theme="dark"])' % pre, light)),
        "}",
        block(':root%s[data-theme="light"]' % pre, light),
        "@media (prefers-contrast: more) {",
        nest(block(dark_sel, dark_more)),
        "}",
        "@media (prefers-contrast: more) and (prefers-color-scheme: light) {",
        nest(block(':root%s:not([data-theme="dark"])' % pre, light_more)),
        "}",
        "@media (prefers-contrast: more) {",
        nest(block(':root%s[data-theme="light"]' % pre, light_more)),
        "}",
        block(':root%s[data-theme="dark"][data-contrast="more"]' % pre, dark_more),
        block(':root%s[data-theme="light"][data-contrast="more"]' % pre, light_more),
        "",
    ]
    return "\n".join(parts)


def write_css(built):
    parts = [
        "/* Hali design language v%s tokens. Generated by scripts/build_tokens.py. Do not edit by hand. */" % VERSION,
        "",
        "/* Static tokens: type, space, shape, size, motion, layers */",
        static_css(),
        "",
        "/* Palettes. Polar is the default. Pick another with data-palette on <html>: aurora, ember, midnight, nord. */",
        "/* Dark is the default theme. Light follows the system, or is set with data-theme. */",
        "",
    ]
    for name in PALETTES:
        d, l, dm, lm = built[name]
        parts.append(palette_css(name, d, l, dm, lm))
    parts += [
        "@media (prefers-reduced-motion: reduce) {",
        "  :root {",
        "    --hali-duration-micro: 0ms;",
        "    --hali-duration-fast: 0ms;",
        "    --hali-duration-productive: 0ms;",
        "    --hali-duration-base: 0ms;",
        "    --hali-duration-slow: 0ms;",
        "    --hali-duration-expressive: 0ms;",
        "    --hali-duration-deliberate: 0ms;",
        "  }",
        "}",
        "",
        "/* The color-scheme hint keeps native controls and scrollbars in step with the theme */",
        ':root, :root[data-theme="dark"] { color-scheme: dark; }',
        '@media (prefers-color-scheme: light) { :root:not([data-theme="dark"]) { color-scheme: light; } }',
        ':root[data-theme="light"] { color-scheme: light; }',
        "",
    ]
    with open(os.path.join(OUT_DIR, "hali-tokens.css"), "w") as f:
        f.write("\n".join(parts))


def write_report(results):
    lines = [
        "# Hali contrast report",
        "",
        "Generated by `scripts/build_tokens.py` for v%s. Targets: primary text 7:1, secondary text 6:1," % VERSION,
        "minimum for all readable text 4.5:1, icons, borders and focus rings 3:1.",
        "",
        "Status and accent text is guaranteed 4.5:1 on the four core surfaces (sunken, default, raised,",
        "overlay) and on its own tonal container, and 3:1 on `surface.strong`.",
        "",
        "Every palette is checked in dark and light. The tables below list each one.",
        "",
    ]
    for key, rows in results.items():
        fails = [r for r in rows if r[4] < r[3]]
        lines.append("## %s (%d checks, %d failing)" % (key, len(rows), len(fails)))
        lines.append("")
        lines.append("| Pairing | Foreground | Background | Ratio | Target | Result |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for label, fg, bg, target, ratio in rows:
            lines.append("| %s | `%s` | `%s` | %.2f | %.1f | %s |" % (
                label, fg, bg, ratio, target, "pass" if ratio >= target else "FAIL"))
        lines.append("")
    with open(os.path.join(OUT_DIR, "CONTRAST.md"), "w") as f:
        f.write("\n".join(lines))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    built = {}
    results = {}
    failures = 0
    for name, (label, note, N, light_from) in PALETTES.items():
        dark, dark_checks, dark_more = build_theme("dark", N)
        LN = PALETTES[light_from][2] if light_from else N
        light, light_checks, light_more = build_theme("light", LN)
        built[name] = (dark, light, dark_more, light_more)
        for mode, checks in (("dark", dark_checks), ("light", light_checks)):
            rows = []
            for lab, fg, bg, target in checks:
                ratio = contrast(fg, bg)
                rows.append((lab, fg, bg, target, ratio))
                if ratio < target:
                    failures += 1
                    print("FAIL [%s %s] %s: %.2f < %.1f (%s on %s)" % (name, mode, lab, ratio, target, fg, bg))
            results["%s %s" % (label, mode)] = rows

    dflt = built[DEFAULT_PALETTE]
    payload = {
        "$meta": {
            "name": "Hali",
            "version": VERSION,
            "description": "A dark first design language for web applications: soft where you touch, crisp where you read. Atlassian structure, Material 3 tonal depth, IBM Carbon rigor.",
            "contrast": {"text-primary": AAA, "text-secondary": SECONDARY, "text-min": AA, "ui": UI},
            "default-theme": "dark",
            "default-palette": DEFAULT_PALETTE,
        },
        "theme": {"dark": dflt[0], "light": dflt[1]},
        "contrast-more": {"dark": dflt[2], "light": dflt[3]},
        "palettes": {
            name: {"label": PALETTES[name][0], "note": PALETTES[name][1],
                   "dark": b[0], "light": b[1], "contrast-more": {"dark": b[2], "light": b[3]}}
            for name, b in built.items()
        },
        "static": STATIC,
    }
    with open(os.path.join(OUT_DIR, "hali-tokens.json"), "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")

    write_css(built)
    write_report(results)

    total = sum(len(r) for r in results.values())
    print("Wrote tokens/hali-tokens.json, tokens/hali-tokens.css, tokens/CONTRAST.md")
    print("%d checks, %d failing" % (total, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
