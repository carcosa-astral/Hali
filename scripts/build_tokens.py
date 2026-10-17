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

from hali_color import BLACK, WHITE, contrast, ensure, mix, rgba, shift_l, soften  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "tokens")

VERSION = "1.0.0"

# ---------------------------------------------------------------------------------------------
# Stock Nord palette (https://www.nordtheme.com/docs/colors-and-palettes)
# ---------------------------------------------------------------------------------------------
NORD = {
    "nord0": "#2E3440", "nord1": "#3B4252", "nord2": "#434C5E", "nord3": "#4C566A",
    "nord4": "#D8DEE9", "nord5": "#E5E9F0", "nord6": "#ECEFF4",
    "nord7": "#8FBCBB", "nord8": "#88C0D0", "nord9": "#81A1C1", "nord10": "#5E81AC",
    "nord11": "#BF616A", "nord12": "#D08770", "nord13": "#EBCB8B", "nord14": "#A3BE8C",
    "nord15": "#B48EAD",
}

STATUS_RAW = {
    "danger": NORD["nord11"],
    "warning": NORD["nord13"],
    "success": NORD["nord14"],
    "info": NORD["nord10"],
    "discovery": NORD["nord15"],
}

ACCENT_RAW = {
    "teal": NORD["nord7"],
    "cyan": NORD["nord8"],
    "blue": NORD["nord10"],
    "red": NORD["nord11"],
    "orange": NORD["nord12"],
    "yellow": NORD["nord13"],
    "green": NORD["nord14"],
    "purple": NORD["nord15"],
}

SURFACE_ORDER = ["sunken", "default", "raised", "overlay", "strong"]

# Contrast targets
AAA = 7.0        # primary text
SECONDARY = 6.0  # secondary text
AA = 4.5         # minimum for all readable text
UI = 3.0         # icons, borders, focus rings, large text


def build_theme(mode):
    """Return (tokens, checks, increased-contrast overrides) for 'dark' or 'light'.

    checks is a list of (label, foreground, background, minimum) tuples.
    """
    dark = mode == "dark"
    direction = 1 if dark else -1  # which way colors move to gain contrast
    t = {}
    checks = []

    # ---- Surfaces: Atlassian names, Material style tonal steps --------------------------------
    if dark:
        t["surface.sunken"] = mix(NORD["nord0"], BLACK, 0.14)
        t["surface.default"] = NORD["nord0"]
        t["surface.raised"] = mix(NORD["nord0"], NORD["nord1"], 0.5)
        t["surface.overlay"] = NORD["nord1"]
        t["surface.strong"] = NORD["nord2"]
    else:
        t["surface.sunken"] = NORD["nord5"]
        t["surface.default"] = NORD["nord6"]
        t["surface.raised"] = mix(NORD["nord6"], WHITE, 0.6)
        t["surface.overlay"] = mix(NORD["nord6"], WHITE, 0.85)
        t["surface.strong"] = NORD["nord4"]

    surfaces = [t["surface." + n] for n in SURFACE_ORDER]
    core = surfaces[:4]  # every surface except the strong hover and selected fill
    strong = t["surface.strong"]
    base = t["surface.default"]

    # ---- Text -------------------------------------------------------------------------------
    if dark:
        t["text.default"] = NORD["nord6"]
        t["text.subtle"] = soften(NORD["nord6"], NORD["nord3"], core, SECONDARY)
        t["text.subtlest"] = soften(NORD["nord4"], NORD["nord3"], core, AA)
        t["text.disabled"] = soften(NORD["nord4"], NORD["nord3"], [base], 2.6)
        t["text.inverse"] = NORD["nord0"]
    else:
        t["text.default"] = NORD["nord0"]
        t["text.subtle"] = soften(NORD["nord0"], NORD["nord6"], core, SECONDARY)
        t["text.subtlest"] = soften(NORD["nord0"], NORD["nord6"], core, AA)
        t["text.disabled"] = soften(NORD["nord0"], NORD["nord6"], [base], 2.6)
        t["text.inverse"] = NORD["nord6"]

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
        t["border.default"] = NORD["nord3"]
        t["border.strong"] = soften(NORD["nord4"], NORD["nord0"], core, UI)
    else:
        t["border.default"] = mix(NORD["nord4"], NORD["nord3"], 0.15)
        t["border.strong"] = soften(NORD["nord3"], NORD["nord6"], core, UI)
    for s in SURFACE_ORDER[:4]:
        checks.append(("border.strong on surface.%s" % s, t["border.strong"], t["surface." + s], UI))

    # ---- Brand (Frost) ----------------------------------------------------------------------
    if dark:
        t["brand.on-bold"] = NORD["nord0"]
        t["brand.bold"] = shift_l(NORD["nord8"], direction, [t["brand.on-bold"]], AA)
        t["brand.bold.hover"] = mix(t["brand.bold"], WHITE, 0.12)
        t["brand.bold.pressed"] = mix(t["brand.bold"], NORD["nord0"], 0.14)
        t["brand.text"] = shift_l(NORD["nord8"], direction, surfaces, AA)
        t["brand.container"] = mix(base, NORD["nord8"], 0.20)
        t["brand.on-container"] = ensure(
            mix(NORD["nord6"], NORD["nord8"], 0.25), NORD["nord6"], [t["brand.container"]], AAA)
    else:
        t["brand.on-bold"] = NORD["nord6"]
        t["brand.bold"] = shift_l(NORD["nord10"], direction, [t["brand.on-bold"]], AA)
        t["brand.bold.hover"] = mix(t["brand.bold"], NORD["nord0"], 0.12)
        t["brand.bold.pressed"] = mix(t["brand.bold"], NORD["nord0"], 0.24)
        t["brand.text"] = shift_l(NORD["nord10"], direction, surfaces, AA)
        t["brand.container"] = mix(base, NORD["nord8"], 0.30)
        t["brand.on-container"] = ensure(
            mix(NORD["nord0"], NORD["nord10"], 0.30), NORD["nord0"], [t["brand.container"]], AAA)

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
    for name, raw in STATUS_RAW.items():
        container = mix(base, raw, 0.15 if dark else 0.16)
        t["%s.container" % name] = container
        text_bgs = core + [container]
        if dark:
            t["%s.on-bold" % name] = NORD["nord0"]
            t["%s.bold" % name] = shift_l(raw, direction, [NORD["nord0"]], AA)
        elif name == "warning":
            t["%s.on-bold" % name] = NORD["nord0"]
            t["%s.bold" % name] = shift_l(raw, 1, [NORD["nord0"]], AA)
        else:
            t["%s.on-bold" % name] = NORD["nord6"]
            t["%s.bold" % name] = shift_l(raw, direction, [NORD["nord6"]], AA)
        t["%s.text" % name] = shift_l(raw, direction, text_bgs, AA)
        for s in SURFACE_ORDER[:4]:
            checks.append(("%s.text on surface.%s" % (name, s), t["%s.text" % name], t["surface." + s], AA))
        checks.append(("%s.text on surface.strong" % name, t["%s.text" % name], strong, UI))
        checks.append(("%s.text on %s.container" % (name, name), t["%s.text" % name], container, AA))
        checks.append(("%s.on-bold on %s.bold" % (name, name), t["%s.on-bold" % name], t["%s.bold" % name], AA))

    # ---- Accents (labels, avatars, chart marks) ---------------------------------------------
    for name, raw in ACCENT_RAW.items():
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

    # ---- State layers, scrim, shadows -------------------------------------------------------
    if dark:
        t["state.hover"] = rgba(NORD["nord6"], 0.08)
        t["state.pressed"] = rgba(NORD["nord6"], 0.14)
        t["state.scrim"] = rgba("#1B1F27", 0.62)
        t["shadow.raised"] = "0 1px 2px rgba(0, 0, 0, 0.30), 0 1px 3px rgba(0, 0, 0, 0.20)"
        t["shadow.overlay"] = "0 4px 12px rgba(0, 0, 0, 0.35), 0 2px 4px rgba(0, 0, 0, 0.25)"
        t["shadow.modal"] = "0 12px 32px rgba(0, 0, 0, 0.45), 0 4px 8px rgba(0, 0, 0, 0.30)"
    else:
        t["state.hover"] = rgba(NORD["nord0"], 0.07)
        t["state.pressed"] = rgba(NORD["nord0"], 0.12)
        t["state.scrim"] = rgba(NORD["nord0"], 0.45)
        t["shadow.raised"] = "0 1px 2px rgba(46, 52, 64, 0.10), 0 1px 3px rgba(46, 52, 64, 0.08)"
        t["shadow.overlay"] = "0 4px 12px rgba(46, 52, 64, 0.14), 0 2px 4px rgba(46, 52, 64, 0.08)"
        t["shadow.modal"] = "0 12px 32px rgba(46, 52, 64, 0.20), 0 4px 8px rgba(46, 52, 64, 0.10)"

    # ---- Raw Nord reference (for charts, syntax themes, brand art) --------------------------
    for k, v in NORD.items():
        t["nord.%s" % k[4:]] = v

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
        "sans": '"Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        "mono": '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace',
    },
    # role: (family, weight, size px, line height px, tracking em)
    "type": {
        "display": ("sans", 600, 40, 48, -0.02),
        "headline-lg": ("sans", 600, 32, 40, -0.015),
        "headline-md": ("sans", 600, 28, 36, -0.01),
        "headline-sm": ("sans", 600, 24, 32, -0.005),
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
    "radius": {"xs": 4, "sm": 6, "md": 8, "lg": 12, "xl": 16, "2xl": 28, "full": 9999},
    "size": {
        "control-sm": 28, "control-md": 36, "control-lg": 44,
        "icon-sm": 16, "icon-md": 20, "icon-lg": 24,
    },
    "motion": {
        "duration": {"fast": 100, "base": 200, "slow": 300, "deliberate": 500},
        "easing": {
            "standard": "cubic-bezier(0.2, 0, 0, 1)",
            "enter": "cubic-bezier(0.05, 0.7, 0.1, 1)",
            "exit": "cubic-bezier(0.3, 0, 0.8, 0.15)",
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
    out["--hali-font-sans"] = STATIC["font"]["sans"]
    out["--hali-font-mono"] = STATIC["font"]["mono"]
    for role, (fam, weight, size, line, track) in STATIC["type"].items():
        out["--hali-type-%s" % role] = "%d %dpx/%dpx var(--hali-font-%s)" % (weight, size, line, fam)
        out["--hali-tracking-%s" % role] = "%gem" % track
    for n in STATIC["space"]:
        out["--hali-space-%d" % n] = "%dpx" % n
    for k, v in STATIC["radius"].items():
        out["--hali-radius-%s" % k] = "%dpx" % v
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


def write_css(dark, light, dark_more, light_more):
    parts = [
        "/* Hali design language v%s tokens. Generated by scripts/build_tokens.py. Do not edit by hand. */" % VERSION,
        "",
        "/* Static tokens: type, space, shape, size, motion, layers */",
        static_css(),
        "",
        "/* Dark is the default theme (Nord first) */",
        block(':root,\n:root[data-theme="dark"]', dark),
        "",
        "/* Light follows the system when no theme is chosen */",
        "@media (prefers-color-scheme: light) {",
        nest(block(':root:not([data-theme="dark"])', light)),
        "}",
        "",
        "/* Light when chosen explicitly */",
        block(':root[data-theme="light"]', light),
        "",
        "/* Increased contrast: follows the system, or opt in with data-contrast=\"more\" */",
        "@media (prefers-contrast: more) {",
        nest(block(':root,\n:root[data-theme="dark"]', dark_more)),
        "}",
        "@media (prefers-contrast: more) and (prefers-color-scheme: light) {",
        nest(block(':root:not([data-theme="dark"])', light_more)),
        "}",
        "@media (prefers-contrast: more) {",
        nest(block(':root[data-theme="light"]', light_more)),
        "}",
        block(':root[data-theme="dark"][data-contrast="more"]', dark_more),
        block(':root[data-theme="light"][data-contrast="more"]', light_more),
        "",
        "@media (prefers-reduced-motion: reduce) {",
        "  :root {",
        "    --hali-duration-fast: 0ms;",
        "    --hali-duration-base: 0ms;",
        "    --hali-duration-slow: 0ms;",
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
    ]
    for mode, rows in results.items():
        fails = [r for r in rows if r[4] < r[3]]
        lines.append("## %s theme (%d checks, %d failing)" % (mode.capitalize(), len(rows), len(fails)))
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
    dark, dark_checks, dark_more = build_theme("dark")
    light, light_checks, light_more = build_theme("light")

    results = {}
    failures = 0
    for mode, checks in (("dark", dark_checks), ("light", light_checks)):
        rows = []
        for label, fg, bg, target in checks:
            ratio = contrast(fg, bg)
            rows.append((label, fg, bg, target, ratio))
            if ratio < target:
                failures += 1
                print("FAIL [%s] %s: %.2f < %.1f (%s on %s)" % (mode, label, ratio, target, fg, bg))
        results[mode] = rows

    payload = {
        "$meta": {
            "name": "Hali",
            "version": VERSION,
            "description": "A dark first, Nord based design language that blends Atlassian structure with Material 3 tonal surfaces.",
            "contrast": {"text-primary": AAA, "text-secondary": SECONDARY, "text-min": AA, "ui": UI},
            "default-theme": "dark",
        },
        "theme": {"dark": dark, "light": light},
        "contrast-more": {"dark": dark_more, "light": light_more},
        "static": STATIC,
    }
    with open(os.path.join(OUT_DIR, "hali-tokens.json"), "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")

    write_css(dark, light, dark_more, light_more)
    write_report(results)

    total = sum(len(r) for r in results.values())
    print("Wrote tokens/hali-tokens.json, tokens/hali-tokens.css, tokens/CONTRAST.md")
    print("%d checks, %d failing" % (total, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
