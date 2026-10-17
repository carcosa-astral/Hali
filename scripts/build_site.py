#!/usr/bin/env python3
"""Build the Hali reference site.

Writes one self-contained file, site/index.html: the tokens, the component CSS, the icon sprite and
the optional behavior script are all inlined, so the file can be opened directly or hosted anywhere.
The site is built from the same files it documents. Run build_tokens.py first.

Run from the repository root:

    python3 scripts/build_site.py
"""

import html
import json
import os
import re
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_tokens  # noqa: E402
import site_assets as A  # noqa: E402
import site_content as C  # noqa: E402
from hali_color import contrast  # noqa: E402

ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "site")
OUT = os.path.join(OUT_DIR, "index.html")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


VERSION = read("VERSION").strip()
TOKENS = json.loads(read("tokens/hali-tokens.json"))
DARK = TOKENS["theme"]["dark"]
LIGHT = TOKENS["theme"]["light"]
STATIC = TOKENS["static"]
SPRITE = read("icons/hali-icons.svg")
ICON_IDS = re.findall(r'<symbol id="(i-[^"]+)"', SPRITE)

_, DARK_CHECKS, _ = build_tokens.build_theme("dark")
_, LIGHT_CHECKS, _ = build_tokens.build_theme("light")

esc = html.escape
I = C.I


# ---------------------------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------------------------

def inline_md(text):
    """Escape text and turn `code`, **bold** and [links](url) into HTML."""
    out = esc(text, quote=False)
    out = re.sub(r"`([^`]+)`", r'<code class="h-code">\1</code>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    return out


def css_var(token):
    return "--hali-" + token.replace(".", "-")


def is_hex(value):
    return bool(re.fullmatch(r"#[0-9A-Fa-f]{6}", value))


def ratio(fg, bg):
    return contrast(fg, bg)


def pass_lozenge(value, target):
    if value >= target:
        return '<span class="h-lozenge h-is-success">%s Pass</span>' % I("check")
    return '<span class="h-lozenge h-is-danger">%s Fail</span>' % I("error")


def code_block(src, open_=False):
    code = textwrap.dedent(src).strip("\n")
    return (
        '<details class="doc-code"%s><summary>%s View code</summary>'
        '<div class="doc-code__body"><button class="h-button h-button--sm h-button--outline doc-copy" '
        'type="button" data-copy>Copy</button><pre class="h-codeblock"><code>%s</code></pre></div></details>'
        % (" open" if open_ else "", I("chevron-right", "h-icon--sm"), esc(code))
    )


def demo(label, src, opts=None):
    opts = opts or {}
    cls = "doc-preview"
    if opts.get("bg"):
        cls += " doc-preview--" + opts["bg"]
    style = ' style="min-height:%s"' % opts["minheight"] if opts.get("minheight") else ""
    inner = textwrap.dedent(src).strip("\n")
    if opts.get("width"):
        inner = '<div style="max-width:%s">%s</div>' % (opts["width"], inner)
    return (
        '<div class="doc-demo"><div class="doc-demo__label">%s</div>'
        '<div class="%s"%s>%s</div>%s</div>' % (esc(label), cls, style, inner, code_block(src))
    )


def swatch(token, dark_value=None, light_value=None, label=None):
    dv = dark_value or DARK[token]
    lv = light_value or LIGHT[token]
    chip = "var(%s)" % css_var(token)
    return (
        '<div class="doc-swatch"><div class="doc-swatch__chip" style="background:%s"></div>'
        '<div class="doc-swatch__meta"><div class="doc-swatch__name">%s</div>'
        '<div class="doc-swatch__var">%s</div>'
        '<div class="doc-swatch__vals"><b>Dark</b> %s<br><b>Light</b> %s</div></div></div>'
        % (chip, esc(label or token), css_var(token), esc(dv), esc(lv))
    )


def table(headers, rows, cls="", wrap_cls="doc-table"):
    head = "".join('<th scope="col"%s>%s</th>' % (' data-numeric' if h.startswith(">") else "", esc(h.lstrip(">")))
                   for h in headers)
    body = ""
    for row in rows:
        cells = ""
        for i, cell in enumerate(row):
            num = " data-numeric" if headers[i].startswith(">") else ""
            cells += "<td%s>%s</td>" % (num, cell)
        body += "<tr>%s</tr>" % cells
    return (
        '<div class="%s"><div class="h-table-wrap"><table class="h-table %s"><thead><tr>%s</tr></thead>'
        '<tbody>%s</tbody></table></div></div>' % (wrap_cls, cls, head, body)
    )


def ul(items, cls="doc-list"):
    return '<ul class="%s">%s</ul>' % (cls, "".join("<li>%s</li>" % inline_md(i) for i in items))


# ---------------------------------------------------------------------------------------------
# Page model
# ---------------------------------------------------------------------------------------------

class Page:
    def __init__(self):
        self.groups = []
        self.parts = []

    def group(self, name):
        self.groups.append((name, []))

    def section(self, sid, title, body, lead=None, nav_label=None, level=2):
        self.groups[-1][1].append((sid, nav_label or title))
        lead_html = '<p class="doc-lead">%s</p>' % inline_md(lead) if lead else ""
        tag = "h%d" % level
        cls = "doc-h2" if level == 2 else "doc-h3"
        extra = " doc-section--component" if level == 3 else ""
        heading = '<%s class="%s">%s</%s>' % (tag, cls, esc(title), tag) if title else ""
        self.parts.append(
            '<section id="%s" class="doc-section%s" data-spy><div class="doc-wrap">%s%s%s</div></section>'
            % (sid, extra, heading, lead_html, body)
        )

    def nav_html(self):
        out = ['<div class="doc-nav__filter"><label class="h-sr-only" for="nav-filter">Filter pages</label>'
               '<div class="h-input-group">%s<input class="h-input h-input--sm" id="nav-filter" type="search" '
               'placeholder="Filter pages" autocomplete="off"></div></div>' % I("search")]
        for name, items in self.groups:
            links = "".join('<a href="#%s">%s</a>' % (sid, esc(label)) for sid, label in items)
            out.append('<div class="doc-nav__section"><div class="doc-nav__group">%s</div>%s</div>' % (esc(name), links))
        return "".join(out)


P = Page()


# ---------------------------------------------------------------------------------------------
# Start
# ---------------------------------------------------------------------------------------------

def overview():
    semantic = len([k for k in DARK if not k.startswith("nord.")])
    checks = len(DARK_CHECKS) + len(LIGHT_CHECKS)
    failing = [c for c in DARK_CHECKS + LIGHT_CHECKS if contrast(c[1], c[2]) < c[3]]
    if failing:
        raise SystemExit("Refusing to build the site: %d contrast checks are failing." % len(failing))
    stats = [
        (str(semantic), "color tokens per theme"),
        (str(len(C.COMPONENTS)), "documented components"),
        (str(len(ICON_IDS)), "icons"),
        (str(checks), "contrast checks, all passing"),
    ]
    stat_html = "".join(
        '<div class="doc-stat"><div class="doc-stat__value">%s</div><div class="doc-stat__label">%s</div></div>' % (v, l)
        for v, l in stats)
    borrow = [
        ("Nord", "Identity",
         "The palette, the cool Polar Night surfaces and the Frost accent. Every color in Hali traces back to a Nord value."),
        ("Atlassian", "Structure",
         "Tokens named by role, bold and subtle emphasis, a 4px grid with a 14px body, lozenges and section messages."),
        ("Material 3", "Surfaces and shape",
         "Tonal elevation, container colors, state layers, type role names, window size classes and expressive easing."),
    ]
    borrow_html = "".join(
        '<div class="h-card"><div class="h-label-md h-text-brand">%s</div><h3 class="h-card__title h-mt-4">%s</h3>'
        '<p class="h-card__meta" style="font-size:14px;line-height:20px">%s</p></div>' % (a, b, c) for a, b, c in borrow)
    body = """
<div class="doc-hero">
  <div class="h-cluster">%(mark)s<span class="h-lozenge h-is-brand">Version %(v)s</span><span class="h-lozenge">Dark first</span><span class="h-lozenge h-is-success">%(check)s WCAG AA and AAA text</span></div>
  <h1 class="doc-hero__title">Hali</h1>
  <p class="doc-lead">A dark first design language for web applications. Nord at its core, Atlassian structure,
  Material 3 tonal surfaces, readable by default. Named for Lake Hali: cold, still, and deep.</p>
  <div class="h-cluster h-mt-24">
    <a class="h-button h-button--bold h-button--lg" href="#getting-started" style="text-decoration:none">Get started %(arrow)s</a>
    <a class="h-button h-button--tonal h-button--lg" href="#actions-button" style="text-decoration:none">Browse components</a>
    <a class="h-button h-button--subtle h-button--lg" href="#changelog" style="text-decoration:none">What is new in %(v)s</a>
  </div>
  <div class="doc-stats">%(stats)s</div>
  <div class="h-grid h-mt-32" style="--h-col:240px">%(borrow)s</div>
</div>""" % {"mark": C.MARK("h-icon--lg h-icon--brand"), "v": VERSION, "check": I("check"),
             "arrow": I("arrow-right"), "stats": stat_html, "borrow": borrow_html}
    P.section("overview", None, body, nav_label="Overview")


def getting_started():
    s1 = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <link rel="stylesheet" href="tokens/hali-tokens.css">
  <link rel="stylesheet" href="css/hali.css">
</head>
<body>
  <!-- Paste icons/hali-icons.svg here once, then use icons with <use href="#i-search"/> -->
  <main class="h-page">
    <h1 class="h-page-header__title">Hello, Hali</h1>
    <button class="h-button h-button--bold">Create project</button>
  </main>
  <script src="js/hali.js" defer></script>
</body>
</html>"""
    s2 = """<html data-theme="dark">                              <!-- default -->
<html data-theme="light">
<html data-theme="light" data-contrast="more">       <!-- increased contrast -->
<html>                                               <!-- dark, or light if the system asks for it -->"""
    s3 = """.my-panel {
  background: var(--hali-surface-raised);
  color: var(--hali-text-default);
  border: 1px solid var(--hali-border-default);
  border-radius: var(--hali-radius-lg);
  padding: var(--hali-space-16);
  box-shadow: var(--hali-shadow-raised);
}
.my-panel__hint { color: var(--hali-text-subtle); font: var(--hali-type-body-sm); }"""
    body = """
<h3 class="doc-h4">1. Add the files</h3>
<p class="doc-p">Hali is plain CSS, an SVG sprite and an optional script. Copy the <code class="h-code">tokens</code>, <code class="h-code">css</code>, <code class="h-code">icons</code> and <code class="h-code">js</code> folders into your project, or add the repository as a Git submodule. Load the tokens first.</p>
%s
<h3 class="doc-h4">2. Choose a theme</h3>
<p class="doc-p">Dark is the default. Set an attribute on the root element to choose explicitly. With no attribute Hali is dark, and it switches to light only when the system asks for it. <code class="h-code">prefers-contrast: more</code> is honored automatically.</p>
%s
<h3 class="doc-h4">3. Use tokens in your own CSS</h3>
<p class="doc-p">Components cover most of a screen. For everything else, use semantic tokens and never a hex value, so themes keep working.</p>
%s
<h3 class="doc-h4">Browser support</h3>
<p class="doc-p">Current evergreen browsers: Chrome and Edge 111 or newer, Safari 16.4 or newer, Firefox 113 or newer. Hali uses cascade layers, <code class="h-code">:has()</code>, <code class="h-code">color-mix()</code> and CSS masks. Fonts are named in the stacks but not bundled: add Inter and JetBrains Mono, or let the system fonts through.</p>
""" % (code_block(s1, True), code_block(s2, True), code_block(s3, True))
    P.section("getting-started", "Getting started", body,
              lead="Three steps from an empty page to a themed screen. No build tool needed.")


def principles():
    items = [
        ("Dark first, light supported", "Design in dark. Derive light. Dark is the default theme and the one every decision is made in."),
        ("Readable always", "7:1 for primary text, 6:1 for secondary text, never below 4.5:1 for anything readable, 3:1 for icons, borders and focus."),
        ("Calm density", "A 14px body, a 4px grid and 36px controls. Quiet, not sparse."),
        ("Tone over shadow", "Depth comes from tonal surface steps. Shadows are kept for things that float."),
        ("One source of truth", "Tokens are generated, checked and shipped as JSON and CSS. Nothing hard codes a color."),
    ]
    cards = "".join(
        '<div class="h-card"><div class="h-label-md h-text-brand">%d</div><h3 class="h-card__title h-mt-4">%s</h3>'
        '<p class="h-card__meta" style="font-size:14px;line-height:20px">%s</p></div>' % (i + 1, t, d)
        for i, (t, d) in enumerate(items))
    blend = table(
        ["Topic", "Atlassian contributes", "Material 3 contributes", "Hali does"],
        [
            ["Token names", "Roles: text, surface, border, brand", "Role pairs: a color and its on-color", "Role names, plus <code class=\"h-code\">on-bold</code> pairs for every filled color"],
            ["Surfaces", "Default, raised, overlay, sunken", "Five tonal container steps", "Five tonal steps with Atlassian names"],
            ["Emphasis", "Bold and subtle", "Filled, tonal, outlined, text", "Bold, tonal, default, outline, subtle"],
            ["Shape", "Small, tight radii", "A range from small to fully round", "8px controls, 12px cards, 16px dialogs, pills for chips and badges"],
            ["Type", "14px body, compact line heights", "Display, headline, title, body, label roles", "Material role names at Atlassian sizes"],
            ["Spacing and density", "8px base with 4px half steps", "4px grid, 40px controls", "4px grid, 36px default control"],
            ["Interaction states", "Distinct hover and pressed colors", "State layers at 8 and 10 percent", "State layers, with dedicated hover tokens on bold fills"],
            ["Motion", "Restrained and quick", "Standard and emphasized easing", "Material curves, 100 to 500ms, zero under reduced motion"],
            ["Breakpoints", "Fluid containers", "Window size classes", "Material window size classes: 600, 840, 1200, 1600"],
        ])
    body = ('<div class="h-grid" style="--h-col:260px">%s</div>'
            '<h3 class="doc-h3">How Atlassian and Material 3 are blended</h3>'
            '<p class="doc-p">Hali is not a mix of two looks. It takes the part each system does best: Atlassian for naming, hierarchy and density, Material 3 for surfaces, state and shape.</p>%s' % (cards, blend))
    P.section("principles", "Principles", body, lead="Five rules that settle most design questions.")


# ---------------------------------------------------------------------------------------------
# Foundations
# ---------------------------------------------------------------------------------------------

NORD_GROUPS = [
    ("Polar Night", ["nord0", "nord1", "nord2", "nord3"], "Dark surfaces. The base of every dark theme."),
    ("Snow Storm", ["nord4", "nord5", "nord6"], "Light text in dark, light surfaces in light."),
    ("Frost", ["nord7", "nord8", "nord9", "nord10"], "The brand. Cool blues and teals."),
    ("Aurora", ["nord11", "nord12", "nord13", "nord14", "nord15"], "Status and accents: red, orange, yellow, green, purple."),
]

STOCK_ROWS = [
    ("dark", "Comment gray as secondary text", "#4C566A", "text.subtlest"),
    ("dark", "Red as error text", "#BF616A", "danger.text"),
    ("dark", "Deep blue as link text", "#5E81AC", "info.text"),
    ("light", "Deep blue as link text", "#5E81AC", "brand.text"),
    ("light", "Yellow as warning text", "#EBCB8B", "warning.text"),
    ("light", "Green as success text", "#A3BE8C", "success.text"),
    ("light", "Orange as accent text", "#D08770", "accent.orange.text"),
    ("light", "Purple as discovery text", "#B48EAD", "discovery.text"),
]

PAIRS = [
    ("Primary text on the page", "text.default", "surface.default", 7.0),
    ("Primary text on the strong fill", "text.default", "surface.strong", 7.0),
    ("Secondary text on a card", "text.subtle", "surface.raised", 6.0),
    ("Tertiary text on a card", "text.subtlest", "surface.raised", 4.5),
    ("Link and brand text on the page", "brand.text", "surface.default", 4.5),
    ("Label on a bold brand button", "brand.on-bold", "brand.bold", 4.5),
    ("Label on the brand container", "brand.on-container", "brand.container", 7.0),
    ("Field border on the page", "border.strong", "surface.default", 3.0),
    ("Focus ring on a card", "border.focus", "surface.raised", 3.0),
    ("Danger text on the page", "danger.text", "surface.default", 4.5),
    ("Warning text on the page", "warning.text", "surface.default", 4.5),
    ("Success text on the page", "success.text", "surface.default", 4.5),
    ("Info text on the page", "info.text", "surface.default", 4.5),
    ("Discovery text on the page", "discovery.text", "surface.default", 4.5),
    ("Danger text on its container", "danger.text", "danger.container", 4.5),
    ("Label on a bold danger button", "danger.on-bold", "danger.bold", 4.5),
    ("Label on a bold warning lozenge", "warning.on-bold", "warning.bold", 4.5),
    ("Label on a bold success lozenge", "success.on-bold", "success.bold", 4.5),
]


def color():
    parts = []

    # Palette
    palette = ""
    for name, keys, note in NORD_GROUPS:
        sw = "".join(
            '<div class="doc-swatch"><div class="doc-swatch__chip" style="background:var(--hali-nord-%s)"></div>'
            '<div class="doc-swatch__meta"><div class="doc-swatch__name">%s</div>'
            '<div class="doc-swatch__var">--hali-nord-%s</div><div class="doc-swatch__vals">%s</div></div></div>'
            % (k[4:], k, k[4:], DARK["nord." + k[4:]]) for k in keys)
        palette += '<h4 class="doc-h4">%s</h4><p class="doc-p h-text-subtle">%s</p><div class="doc-swatches">%s</div>' % (name, note, sw)
    parts.append('<h3 class="doc-h3">The Nord palette</h3><p class="doc-p">Sixteen colors, unchanged. Hali exposes them as <code class="h-code">--hali-nord-0</code> to <code class="h-code">--hali-nord-15</code> for illustration and syntax themes. Interface text and fills never use them directly: they use the semantic tokens below.</p>' + palette)

    # Why tweak
    rows = []
    for mode, label, stock_fg, token in STOCK_ROWS:
        theme = DARK if mode == "dark" else LIGHT
        bg = theme["surface.default"]
        hali_fg = theme[token]
        r1, r2 = ratio(stock_fg, bg), ratio(hali_fg, bg)
        s1 = '<span class="doc-sample" style="color:%s;background:%s;padding:3px 10px;border-radius:6px;white-space:nowrap">Aa Sample</span>' % (stock_fg, bg)
        s2 = '<span class="doc-sample" style="color:%s;background:%s;padding:3px 10px;border-radius:6px;white-space:nowrap">Aa Sample</span>' % (hali_fg, bg)
        rows.append([mode.capitalize(), label, s1, "%.2f:1" % r1, s2, "%.2f:1" % r2, '<code class="h-code">%s</code>' % token])
    why = table(["Theme", "Use", "Stock Nord", ">Ratio", "Hali", ">Ratio", "Token"], rows)
    parts.append('<h3 class="doc-h3">Why Nord needed tweaks</h3><p class="doc-p">Stock Nord is beautiful and a little too quiet. Its comment gray is 1.7:1 on its own background, and most Aurora colors fail on light surfaces. Hali keeps every hue and lifts only what fails. The adjustment happens in OKLCH, so a red stays red and a yellow stays yellow as they gain contrast.</p>' + why)

    # Surfaces
    surf_notes = {
        "sunken": "Inset wells, field backgrounds, code blocks",
        "default": "The page canvas",
        "raised": "Cards, panels, table containers",
        "overlay": "Menus, popovers, dialogs, toasts",
        "strong": "Selected and hover fills, neutral lozenges, default buttons",
    }
    ladder = "".join(
        '<div style="background:var(--hali-surface-%s)"><div><strong>surface.%s</strong><div class="h-body-sm h-text-subtle">%s</div></div>'
        '<code class="h-code">%s</code></div>' % (n, n, d, css_var("surface." + n))
        for n, d in surf_notes.items())
    parts.append('<h3 class="doc-h3">Surfaces</h3><p class="doc-p">Depth is tone. Five steps from lowest to highest. In dark, higher is lighter. In light, <em>raised</em> and <em>overlay</em> are lighter than the page, and <em>sunken</em> and <em>strong</em> are darker.</p><div class="doc-ladder">%s</div><div class="doc-swatches">%s</div>'
                 % (ladder, "".join(swatch("surface." + n) for n in surf_notes)))

    # Text and borders
    text_sw = "".join(swatch(t) for t in ["text.default", "text.subtle", "text.subtlest", "text.disabled", "text.inverse", "icon.default", "icon.subtle", "border.default", "border.strong", "border.focus"])
    parts.append('<h3 class="doc-h3">Text, icons and borders</h3>'
                 '<p class="doc-p"><strong>default</strong> is 7:1 or better on every surface. <strong>subtle</strong> is 6:1 on the core surfaces for secondary text. <strong>subtlest</strong> is 4.5:1 for hints and metadata. <strong>disabled</strong> is deliberately quiet and exempt from contrast rules, so never use it for anything someone needs to read.</p>'
                 '<div class="doc-swatches">%s</div>' % text_sw)

    # Brand
    brand_sw = "".join(swatch(t) for t in ["brand.bold", "brand.bold.hover", "brand.bold.pressed", "brand.on-bold", "brand.text", "brand.container", "brand.on-container"])
    parts.append('<h3 class="doc-h3">Brand</h3><p class="doc-p">The Frost cyan. <strong>bold</strong> is a solid fill with its <strong>on-bold</strong> label. <strong>container</strong> is the quiet tonal version. <strong>text</strong> is for links and text on a surface.</p><div class="doc-swatches">%s</div>' % brand_sw)

    # Status
    fam = ""
    for name in ["danger", "warning", "success", "info", "discovery"]:
        d, l = DARK, LIGHT
        chips = (
            '<span class="doc-chip-bold" style="background:var(--hali-%(n)s-bold);color:var(--hali-%(n)s-on-bold)">%(n)s bold</span>'
            '<span class="doc-chip-container" style="background:var(--hali-%(n)s-container);color:var(--hali-%(n)s-text)">%(n)s container</span>'
            '<span style="color:var(--hali-%(n)s-text);font:var(--hali-type-label-lg)">%(n)s text</span>' % {"n": name})
        fam += ('<div class="doc-family"><div class="h-title-sm" style="text-transform:capitalize">%s</div><div class="doc-family__chips">%s</div>'
                '<div class="doc-ratio">Text on page: dark %.1f:1, light %.1f:1</div></div>'
                % (name, chips, ratio(d[name + ".text"], d["surface.default"]), ratio(l[name + ".text"], l["surface.default"])))
    parts.append('<h3 class="doc-h3">Status</h3><p class="doc-p">Five families from Aurora. Each has <strong>bold</strong>, <strong>on-bold</strong>, <strong>container</strong> and <strong>text</strong>. Never rely on color alone: pair status with an icon or a word.</p><div class="h-grid" style="--h-col:260px">%s</div>' % fam)

    # Accents
    acc = ""
    for name in ["teal", "cyan", "blue", "red", "orange", "yellow", "green", "purple"]:
        acc += ('<div class="doc-family"><div class="h-title-sm" style="text-transform:capitalize">%(n)s</div>'
                '<div class="doc-family__chips"><span class="doc-chip-bold" style="background:var(--hali-accent-%(n)s-fill);color:var(--hali-surface-default)">fill</span>'
                '<span class="doc-chip-container" style="background:var(--hali-accent-%(n)s-container);color:var(--hali-accent-%(n)s-text)">container</span>'
                '<span style="color:var(--hali-accent-%(n)s-text);font:var(--hali-type-label-lg)">text</span></div></div>' % {"n": name})
    parts.append('<h3 class="doc-h3">Accents</h3><p class="doc-p">Eight accents for labels, avatars and chart marks. <strong>fill</strong> meets 3:1 for graphics, <strong>text</strong> meets 4.5:1, and <strong>container</strong> is the tonal background.</p><div class="h-grid" style="--h-col:200px">%s</div>' % acc)

    # Contrast matrix
    mrows = []
    for label, fg, bg, target in PAIRS:
        dr, lr = ratio(DARK[fg], DARK[bg]), ratio(LIGHT[fg], LIGHT[bg])
        mrows.append([label, "<code class=\"h-code\">%s</code> on <code class=\"h-code\">%s</code>" % (fg, bg), "%.1f:1" % target,
                      "%.2f:1 %s" % (dr, pass_lozenge(dr, target)), "%.2f:1 %s" % (lr, pass_lozenge(lr, target))])
    parts.append('<h3 class="doc-h3">Contrast</h3><p class="doc-p">%d pairings are checked on every build in both themes and the build fails if any misses. A selection:</p>%s<p class="doc-p h-text-subtle">The full report is generated at <code class="h-code">tokens/CONTRAST.md</code>.</p>'
                 % (len(DARK_CHECKS) + len(LIGHT_CHECKS), table(["Pairing", "Tokens", ">Target", ">Dark", ">Light"], mrows)))

    P.section("color", "Color", "".join(parts), lead="Nord for identity, tuned for readability. Dark is the default, and every token has a light value.")


def typography():
    samples = {
        "display": "Calm by design", "headline-lg": "Calm interfaces for busy people",
        "headline-md": "Calm interfaces for busy people", "headline-sm": "Calm interfaces for busy people",
        "title-lg": "Project settings", "title-md": "Project settings", "title-sm": "Project settings",
        "body-lg": "Hali keeps dense screens readable with a 14px body, a 4px grid and quiet tonal surfaces.",
        "body-md": "Hali keeps dense screens readable with a 14px body, a 4px grid and quiet tonal surfaces.",
        "body-sm": "Updated 2 hours ago by Ana Ruiz", "label-lg": "Create project", "label-md": "Create project",
        "label-sm": "NEW", "code-md": "--hali-surface-raised",
    }
    rows = ""
    for role, (fam, weight, size, line, track) in STATIC["type"].items():
        rows += ('<div class="doc-type-row"><div class="doc-sample" style="font:var(--hali-type-%(r)s);letter-spacing:var(--hali-tracking-%(r)s)">%(s)s</div>'
                 '<div><code class="h-code">.h-%(r)s</code><div class="h-body-sm h-text-subtle h-mt-4">%(z)dpx / %(l)dpx, weight %(w)d, %(f)s</div></div></div>'
                 % {"r": role, "s": esc(samples[role]), "z": size, "l": line, "w": weight, "f": "tracking %gem" % track})
    fonts = ("<p class=\"doc-p\"><strong>Sans</strong>: <code class=\"h-code\">%s</code></p><p class=\"doc-p\"><strong>Mono</strong>: <code class=\"h-code\">%s</code></p>"
             % (esc(STATIC["font"]["sans"]), esc(STATIC["font"]["mono"])))
    body = ('<h3 class="doc-h3">Typefaces</h3><p class="doc-p">Inter for interface text and JetBrains Mono for code, with the system fonts as the fallback. Neither is bundled, so add them with your own font loading.</p>%s'
            '<h3 class="doc-h3">Type scale</h3><p class="doc-p">Fourteen roles. The names come from Material 3 and the sizes from Atlassian: body text is 14px, headings step up in clear intervals, and labels are medium weight.</p>%s'
            '<h3 class="doc-h3">Guidelines</h3>%s' % (fonts, rows, ul([
                "Choose a role by what the text does, not how big you want it. Use `title` for card and section names, `label` for controls, and `body` for reading.",
                "Keep line length between 45 and 75 characters. `h-prose` caps at 68ch.",
                "Use two weights at most per view: regular and one of medium or semibold.",
                "Use `h-tabular` for numbers that line up in columns or change in place.",
                "Heading classes change how a heading looks, never what it is. Keep one `h1` per page and do not skip levels.",
            ])))
    P.section("typography", "Typography", body, lead="Material role names at Atlassian sizes.")


def spacing():
    use = {
        2: "Hairline gaps, such as a badge against an icon",
        4: "Tight inline gaps",
        6: "Chip and lozenge padding, icon to label in small controls",
        8: "The default gap between related elements",
        12: "Control horizontal padding, gaps inside forms",
        16: "Card padding, page gutter on compact screens",
        20: "Dialog header padding",
        24: "Gap between sections of a card, dialog padding",
        32: "Page gutter from 840px, gap between page sections",
        40: "Large gaps between groups of content",
        48: "Page bottom padding, empty states",
        64: "Major layout separation",
        80: "Hero and marketing spacing",
    }
    rows = "".join(
        '<div class="doc-space-row"><code class="h-code">%d</code><span class="h-body-sm h-text-subtle">%dpx</span>'
        '<div><div class="doc-space-bar" style="width:%dpx"></div><div class="h-body-sm h-text-subtle h-mt-4">%s</div></div></div>'
        % (n, n, n, use[n]) for n in STATIC["space"])
    body = ('<p class="doc-p">Tokens are named by their pixel value: <code class="h-code">--hali-space-16</code> is 16px. Every layout step lands on the 4px grid, with 2px and 6px as the only exceptions for tight inner spacing.</p>%s'
            '<h3 class="doc-h3">Control sizes</h3>%s' % (rows, table(
                ["Token", ">Size", "Use"],
                [['<code class="h-code">--hali-size-control-sm</code>', "28px", "Dense toolbars, table rows"],
                 ['<code class="h-code">--hali-size-control-md</code>', "36px", "Default for buttons and fields"],
                 ['<code class="h-code">--hali-size-control-lg</code>', "44px", "Primary actions, touch layouts. All controls grow to 44px on coarse pointers"]])))
    P.section("spacing", "Spacing", body, lead="A 4px grid with a 14px body. Dense enough to work in, calm enough to read.")


def layout():
    bp = table(
        ["Window class", ">Width", ">Columns", ">Page margin", "Notes"],
        [["Compact", "0 to 599", "4", "16px", "Single column. Side navigation hidden."],
         ["Medium", "600 to 839", "8", "24px", "Side navigation hidden or a rail."],
         ["Expanded", "840 to 1199", "12", "32px", "Side navigation visible. Gutter grows to 24px."],
         ["Large", "1200 to 1599", "12", "32px", "Content stops at 1200px and centers."],
         ["Extra large", "1600 and up", "12", "32px", "Same as large. Extra width becomes margin."]])
    grid = "".join('<div>%d</div>' % i for i in range(1, 13))
    shell = ('<div class="doc-shell-diagram"><div class="doc-shell-diagram__top">Top bar, 56px</div>'
             '<div class="doc-shell-diagram__side">Side nav, 264px</div><div class="doc-shell-diagram__main">Main content, scrolls on its own. Page max width 1120px.</div></div>')
    body = ('<p class="doc-p">Hali uses the Material window size classes. Layout classes are mobile first.</p>%s'
            '<h3 class="doc-h3">Columns</h3><p class="doc-p">Use <code class="h-code">h-columns</code> with <code class="h-code">h-col-*</code> for a 4, 8 or 12 column grid, and <code class="h-code">h-grid</code> for auto fitting cards.</p><div class="doc-bp">%s</div>'
            '<h3 class="doc-h3">Application shell</h3>%s'
            '<h3 class="doc-h3">Layout primitives</h3>%s' % (bp, grid, shell, table(
                ["Class", "Does"],
                [['<code class="h-code">h-container</code>', "Centers content to 1200px with responsive side padding"],
                 ['<code class="h-code">h-stack</code>', "Vertical flow with a consistent gap. Set the gap with <code class=\"h-code\">h-gap-*</code>"],
                 ['<code class="h-code">h-cluster</code>', "Wrapping row for buttons, chips and tags"],
                 ['<code class="h-code">h-split</code>', "Two ends: label on the left, control on the right"],
                 ['<code class="h-code">h-grid</code>', "Auto fitting columns. Set the minimum width with <code class=\"h-code\">--h-col</code>"],
                 ['<code class="h-code">h-appshell</code>', "Top bar, side navigation and main, as a grid"],
                 ['<code class="h-code">h-page</code>', "Padded, width limited main content"]])))
    P.section("layout", "Layout and grid", body, lead="Material window size classes, Atlassian style page structure.")


def shape():
    use = {
        "xs": "Checkboxes, keys, inline code",
        "sm": "Lozenges, skeletons",
        "md": "Buttons, fields, chips, menu items",
        "lg": "Cards, alerts, menus, tables",
        "xl": "Dialogs",
        "2xl": "Reserved for large containers",
        "full": "Badges, avatars, switches, progress",
    }
    cells = "".join(
        '<div class="doc-radius"><div class="doc-radius__box" style="border-radius:%s"></div><div><code class="h-code">%s</code><div class="h-body-sm h-text-subtle">%s</div></div></div>'
        % ("var(--hali-radius-%s)" % k, k, "%spx" % v if v < 1000 else "9999px") for k, v in STATIC["radius"].items())
    rows = [['<code class="h-code">%s</code>' % k, "%dpx" % v if v < 1000 else "full", use[k]] for k, v in STATIC["radius"].items()]
    body = '<div class="doc-radius-grid">%s</div>%s<p class="doc-p">Nested shapes step down: a button inside a card uses a smaller radius than the card, so corners look concentric.</p>' % (cells, table(["Token", ">Radius", "Use"], rows))
    P.section("shape", "Shape", body, lead="Rounded enough to feel soft, restrained enough to feel precise.")


def elevation():
    boxes = "".join(
        '<div class="doc-shadow-box" style="box-shadow:var(--hali-shadow-%s)">%s<div class="h-body-sm h-text-subtle">%s</div></div>' % (n, n, d)
        for n, d in [("raised", "Cards that need to lift"), ("overlay", "Menus and popovers"), ("modal", "Dialogs and sheets")])
    body = ('<p class="doc-p">Hierarchy comes from tone: look at the five surface steps in the Color section. Shadows are reserved for things that float above the page and are only visible against a quiet background.</p>'
            '<div class="doc-shadows">%s</div>%s' % (boxes, ul([
                "A card sitting on the page is `surface.raised` with a border. It needs no shadow.",
                "Menus, popovers and toasts use `surface.overlay` and `shadow.overlay`.",
                "Dialogs and sheets use `surface.overlay`, `shadow.modal` and a scrim.",
                "In light, shadows are tinted with Nord's Polar Night so they stay soft and cool.",
            ])))
    P.section("elevation", "Elevation", body, lead="Tone first. Shadow only for things that float.")


def motion():
    dur_use = {"fast": "Hover and pressed state layers", "base": "Toggles, switches, menus, toasts",
               "slow": "Dialogs, progress changes", "deliberate": "Page level transitions and large moves"}
    ease_use = {"standard": "Most movement and color changes", "enter": "Things appearing on screen, decelerating",
                "exit": "Things leaving the screen, accelerating"}
    rows = ""
    for key, ms in STATIC["motion"]["duration"].items():
        ease = STATIC["motion"]["easing"]["standard"]
        rows += ('<div class="doc-motion-row"><div><code class="h-code">%s</code><div class="h-body-sm h-text-subtle h-mt-4">%dms</div></div>'
                 '<div class="doc-motion-track"><div class="doc-motion-dot"></div></div>'
                 '<button class="h-button h-button--outline h-button--sm" data-motion data-ms="%d" data-ease="%s">Play</button></div>' % (key, ms, ms, ease))
    easing = table(["Token", "Curve", "Use"], [
        ['<code class="h-code">%s</code>' % k, '<code class="h-code">%s</code>' % v, ease_use[k]] for k, v in STATIC["motion"]["easing"].items()])
    durs = table(["Token", ">Duration", "Use"], [
        ['<code class="h-code">%s</code>' % k, "%dms" % v, dur_use[k]] for k, v in STATIC["motion"]["duration"].items()])
    body = ('<p class="doc-p">Motion explains change. It is quick, never decorative, and it disappears for anyone who asks for reduced motion: every duration token becomes 0ms.</p>'
            '<h3 class="doc-h3">Durations</h3>%s<div>%s</div><h3 class="doc-h3">Easing</h3>%s' % (durs, rows, easing))
    P.section("motion", "Motion", body, lead="Material curves, short durations, and none at all when asked.")


def iconography():
    cells = "".join(
        '<button class="doc-icon" type="button" data-snippet=\'%s\' data-name="%s" aria-label="Copy %s icon markup">%s<span>%s</span></button>'
        % (esc('<svg class="h-icon" aria-hidden="true"><use href="#%s"/></svg>' % i, quote=True), i[2:], i[2:], I(i[2:], "h-icon--lg"), i[2:])
        for i in ICON_IDS)
    sizes = demo("Sizes", """
<div class="h-cluster h-gap-24">
  <span class="h-cluster h-gap-8"><svg class="h-icon h-icon--sm" aria-hidden="true"><use href="#i-search"/></svg> 16px</span>
  <span class="h-cluster h-gap-8"><svg class="h-icon" aria-hidden="true"><use href="#i-search"/></svg> 20px</span>
  <span class="h-cluster h-gap-8"><svg class="h-icon h-icon--lg" aria-hidden="true"><use href="#i-search"/></svg> 24px</span>
</div>""")
    body = ('<p class="doc-p">%d line icons on a 24px grid with a 1.75px stroke and round caps. They take their color from the text around them. Click an icon to copy its markup.</p><div class="doc-icons">%s</div>%s%s'
            % (len(ICON_IDS), cells, sizes, ul([
                "Decorative icons get `aria-hidden=\"true\"`. Icon only buttons get an `aria-label` on the button.",
                "Use 16px inside small controls and dense text, 20px by default, 24px for navigation and empty states.",
                "Pair an icon with a label wherever space allows. A bare icon is only as clear as its convention.",
                "Add an icon by drawing it on the 24px grid with a 1.75px stroke, then adding a `symbol` to `icons/hali-icons.svg`.",
            ])))
    P.section("iconography", "Iconography", body, lead="Quiet line icons that inherit color.")


def dataviz():
    series = [
        ("cyan", [20, 34, 30, 48, 52, 68], "Signups"),
        ("orange", [12, 18, 26, 24, 38, 41], "Activations"),
        ("purple", [30, 28, 35, 33, 31, 40], "Upgrades"),
    ]
    dash = ["", "6 4", "2 4"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    left, right, top, bottom = 44, 620, 16, 190
    ymax = 80

    def px(i):
        return left + (right - left) * i / (len(months) - 1)

    def py(v):
        return bottom - (bottom - top) * v / ymax

    svg = ['<svg class="doc-chart" viewBox="0 0 660 232" role="img" aria-label="Line chart of signups, activations and upgrades from January to June">']
    for level in range(0, ymax + 1, 20):
        y = py(level)
        svg.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="var(--hali-border-default)" stroke-width="1"/>' % (left, right, y, y))
        svg.append('<text x="%d" y="%.1f" text-anchor="end">%d</text>' % (left - 8, y + 4, level))
    for i, m in enumerate(months):
        svg.append('<text x="%.1f" y="%d" text-anchor="middle">%s</text>' % (px(i), bottom + 22, m))
    for n, (name, vals, label) in enumerate(series):
        pts = " ".join("%.1f,%.1f" % (px(i), py(v)) for i, v in enumerate(vals))
        d = ' stroke-dasharray="%s"' % dash[n] if dash[n] else ""
        svg.append('<polyline points="%s" fill="none" stroke="var(--hali-accent-%s-fill)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"%s/>' % (pts, name, d))
        for i, v in enumerate(vals):
            x, y = px(i), py(v)
            fill = "var(--hali-accent-%s-fill)" % name
            if n == 0:
                svg.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (x, y, fill))
            elif n == 1:
                svg.append('<rect x="%.1f" y="%.1f" width="8" height="8" fill="%s"/>' % (x - 4, y - 4, fill))
            else:
                svg.append('<path d="M%.1f %.1f l4.5 4.5 l-4.5 4.5 l-4.5 -4.5z" fill="%s"/>' % (x, y - 4.5, fill))
    svg.append("</svg>")
    legend = "".join('<li><i style="background:var(--hali-accent-%s-fill)"></i>%s</li>' % (name, label) for name, _, label in series)
    order = ["cyan", "orange", "purple", "yellow", "green", "red", "blue", "teal"]
    sw = "".join('<span class="doc-chip-bold" style="background:var(--hali-accent-%s-fill);color:var(--hali-surface-default)">%d %s</span>' % (n, i + 1, n) for i, n in enumerate(order))
    body = ('<p class="doc-p">Use the eight accent <strong>fill</strong> colors in this order. Each meets 3:1 against the page, and neighbors in the sequence differ strongly in hue and lightness.</p>'
            '<div class="doc-family__chips h-mt-16">%s</div>'
            '<div class="doc-preview h-mt-24">%s<ul class="doc-legend">%s</ul></div>%s'
            % (sw, "".join(svg), legend, ul([
                "Never encode meaning in color alone. The chart above also changes line style and marker shape per series.",
                "Use six series or fewer. Past that, group, filter or small multiples.",
                "Label lines directly at their ends when there is room, and keep a legend for the rest.",
                "Gridlines use `border.default`. Axis text uses `text.subtle` at the `label-md` size.",
                "Use status colors only for status. A red line should mean something is wrong.",
            ])))
    P.section("data-viz", "Data visualization", body, lead="A color order that stays distinguishable and never depends on color alone.")


def accessibility():
    rows = [
        ["Primary text", "7:1 or better on every surface, in both themes"],
        ["Secondary text", "6:1 or better on the core surfaces"],
        ["Tertiary text", "4.5:1 or better on the core surfaces"],
        ["Status and accent text", "4.5:1 on the core surfaces and its own container, 3:1 on the strong fill"],
        ["Brand text and links", "4.5:1 on every surface"],
        ["Icons, field borders, focus ring", "3:1 against every adjacent surface"],
        ["Focus", "A 2px ring with a 2px offset on every interactive element"],
        ["Targets", "36px default. 44px on coarse pointers. Never below 24px"],
        ["Motion", "Every transition goes to zero under reduced motion"],
        ["Contrast preference", "`prefers-contrast: more` and `data-contrast=\"more\"` raise secondary text and decorative borders"],
        ["Forced colors", "Borders, selected states and focus map to system colors"],
    ]
    t = table(["Area", "Guarantee"], [[a, inline_md(g)] for a, g in rows])
    keys = table(["Pattern", "Keys"], [
        ["Button, link", "Enter, and Space for buttons"],
        ["Tabs", "Left and Right arrows move, Home and End jump. Only the selected tab is in the tab order"],
        ["Menu", "Down opens and moves, Up moves, Home and End jump, Escape closes and returns focus"],
        ["Dialog", "Focus moves in on open and returns on close. Escape closes. Tab stays inside"],
        ["Checkbox, switch", "Space toggles"],
        ["Radio group", "Arrow keys move and select"],
        ["Disclosure", "Enter or Space toggles"],
    ])
    body = ('<p class="doc-p">Hali is designed to meet WCAG 2.2 level AA throughout, and AAA for primary text. These are the guarantees the system makes. Using them correctly still takes correct markup: the documentation for each component lists what it requires.</p>%s'
            '<h3 class="doc-h3">Keyboard patterns</h3>%s'
            '<h3 class="doc-h3">Rules for using the system</h3>%s'
            '<p class="doc-p h-text-subtle">The full checklist every component passes is in <code class="h-code">docs/ACCESSIBILITY.md</code>.</p>' % (t, keys, ul([
                "Never convey meaning by color alone. Status needs an icon or a word as well. Links inside running text keep their underline.",
                "Do not put raw Nord colors on text. Use semantic tokens.",
                "Label every control with a visible `h-label`, or `aria-label` for icon only buttons.",
                "Test with a keyboard, a screen reader, 200 percent zoom, reduced motion and forced colors.",
            ])))
    P.section("accessibility", "Accessibility", body, lead="Readable by default, checked on every build.")


def content():
    principles_html = "".join(
        '<div class="h-card"><h3 class="h-card__title">%s</h3><p class="h-card__meta" style="font-size:14px;line-height:20px">%s</p></div>' % (t, d)
        for t, d in C.VOICE_PRINCIPLES)
    tone = table(["Situation", "Tone", "Example"], [[a, b, esc(c)] for a, b, c in C.TONE_TABLE])
    rules = "".join(
        '<div class="doc-usage" style="grid-template-columns:200px 1fr;margin:0"><div style="border:0;background:none;padding:12px 0"><strong>%s</strong></div><div style="border:0;background:none;padding:12px 0">%s</div></div>' % (t, inline_md(d))
        for t, d in C.WRITING_RULES)
    pairs = "".join(
        '<div class="doc-pair"><div class="doc-pair__do"><div class="doc-pair__tag">%s Do</div>%s</div><div class="doc-pair__dont"><div class="doc-pair__tag">%s Avoid</div>%s</div></div>'
        % (I("check", "h-icon--sm"), esc(a), I("close", "h-icon--sm"), esc(b)) for a, b in C.DO_DONT)
    body = ('<h3 class="doc-h3">Voice</h3><div class="h-grid" style="--h-col:200px">%s</div>'
            '<h3 class="doc-h3">Tone by situation</h3>%s'
            '<h3 class="doc-h3">Writing rules</h3><div class="h-stack h-gap-0" style="border-top:1px solid var(--hali-border-default)">%s</div>'
            '<h3 class="doc-h3">Do and avoid</h3>%s' % (principles_html, tone, rules, pairs))
    P.section("content", "Content and voice", body, lead="Plain, specific and short. Interface text is part of the design.")


# ---------------------------------------------------------------------------------------------
# Components and patterns
# ---------------------------------------------------------------------------------------------

GROUP_ORDER = ["Actions", "Forms", "Display", "Feedback", "Navigation", "Overlays", "Data"]


def components_intro():
    rows = [[esc(a), '<span class="h-lozenge %s">%s</span>' % ("h-is-success" if b == "Stable" else "h-is-neutral", b), c] for a, b, c in C.STATUS_TABLE]
    states = ul([
        "**Default, hover, pressed**: hover and pressed use a state layer at 8 and 14 percent, so every variant responds the same way.",
        "**Focus**: a 2px ring offset by 2px, 3:1 against every surface.",
        "**Disabled**: quiet and intentionally low contrast. Explain why nearby.",
        "**Selected**: a tonal brand fill, never color alone.",
        "**Invalid**: a danger border plus an icon and text.",
        "**Loading**: `aria-busy` with a spinner that replaces the label.",
    ])
    body = ('<p class="doc-p">Every component is documented with live examples, the markup it requires, usage guidance, and its accessibility needs. The code under each example is the exact markup rendered above it.</p>'
            '<h3 class="doc-h3">Status</h3>%s<h3 class="doc-h3">States</h3>%s' % (table(["Components", "Status", "Since"], rows), states))
    P.section("components", "Components", body, lead="%d components across seven groups." % len(C.COMPONENTS), nav_label="Overview and status")


def component_sections():
    ordered = sorted(C.COMPONENTS, key=lambda c: GROUP_ORDER.index(c["group"]))
    current = None
    for c in ordered:
        if c["group"] != current:
            current = c["group"]
            P.group(current)
        parts = []
        for label, src, opts in c["demos"]:
            parts.append(demo(label, src, opts))
        if c["use"] or c["avoid"]:
            parts.append('<div class="doc-usage"><div><h4>%s Use it to</h4>%s</div><div><h4>%s Avoid</h4>%s</div></div>' % (
                I("check", "h-icon--sm"), ul(c["use"], "") if c["use"] else "<p class=\"h-text-subtle\">Nothing specific.</p>",
                I("close", "h-icon--sm"), ul(c["avoid"], "") if c["avoid"] else "<p class=\"h-text-subtle\">Nothing specific.</p>"))
        if c["a11y"]:
            parts.append('<h4 class="doc-h4">Accessibility</h4>' + ul(c["a11y"]))
        P.section("%s-%s" % (c["group"].lower(), c["id"]), c["title"], "".join(parts), lead=c["blurb"], level=3)


def pattern_sections():
    P.group("Patterns")
    for p in C.PATTERNS:
        if p["height"] == "auto":
            preview = '<div class="doc-preview">%s</div>' % textwrap.dedent(p["html"]).strip("\n")
        else:
            preview = '<div class="doc-frame" style="height:%s">%s</div>' % (p["height"], textwrap.dedent(p["html"]).strip("\n"))
        body = '<div class="doc-demo">%s%s</div>' % (preview, code_block(p["html"]))
        if p["notes"]:
            body += ul(p["notes"])
        P.section(p["id"], p["title"], body, lead=p["blurb"], level=3)


# ---------------------------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------------------------

def tokens_section():
    files = table(["File", "What it is"], [
        ['<code class="h-code">tokens/hali-tokens.css</code>', "Every token as a CSS custom property. Dark default, light, and increased contrast."],
        ['<code class="h-code">tokens/hali-tokens.json</code>', "The same tokens as data, for design tools, native apps and build pipelines."],
        ['<code class="h-code">tokens/CONTRAST.md</code>', "Every checked pairing with its ratio."],
        ['<code class="h-code">css/hali.css</code>', "Base, layout, typography, components and utilities, in cascade layers."],
        ['<code class="h-code">js/hali.js</code>', "Optional behavior: tabs, dropdowns, dialogs, chips, segmented controls, sortable tables, toasts."],
        ['<code class="h-code">icons/hali-icons.svg</code>', "The icon sprite and the Hali mark."],
    ])
    rows = []
    for key, dv in DARK.items():
        lv = LIGHT[key]
        dsw = '<span class="doc-dot" style="background:%s"></span>' % dv if is_hex(dv) else ""
        lsw = '<span class="doc-dot" style="background:%s"></span>' % lv if is_hex(lv) else ""
        rows.append('<tr data-token="%s"><td><code class="h-code">%s</code></td><td><code class="h-code">%s</code></td><td>%s%s</td><td>%s%s</td></tr>'
                    % (esc((key + " " + css_var(key)).lower()), esc(key), css_var(key), dsw, esc(dv), lsw, esc(lv)))
    ref = ('<div class="doc-table"><div class="h-table-wrap" style="max-height:520px"><table class="h-table h-table--dense"><thead><tr>'
           '<th scope="col">Token</th><th scope="col">CSS property</th><th scope="col">Dark</th><th scope="col">Light</th></tr></thead><tbody>%s</tbody></table></div></div>' % "".join(rows))
    flt = ('<div class="h-field" style="max-width:360px;margin-top:16px"><label class="h-label" for="token-filter">Filter tokens</label>'
           '<div class="h-input-group">%s<input class="h-input" id="token-filter" type="search" placeholder="surface, danger, brand.bold" autocomplete="off"></div></div>' % I("search"))
    static_rows = [
        ["Type", "%d roles" % len(STATIC["type"]), "`--hali-type-body-md`, `--hali-tracking-body-md`"],
        ["Space", "%d steps" % len(STATIC["space"]), "`--hali-space-16`"],
        ["Radius", "%d steps" % len(STATIC["radius"]), "`--hali-radius-lg`"],
        ["Size", "%d tokens" % len(STATIC["size"]), "`--hali-size-control-md`, `--hali-size-icon-md`"],
        ["Motion", "%d durations, %d curves" % (len(STATIC["motion"]["duration"]), len(STATIC["motion"]["easing"])), "`--hali-duration-base`, `--hali-ease-standard`"],
        ["Layers", "%d levels" % len(STATIC["z"]), "`--hali-z-modal`"],
    ]
    body = ('%s<h3 class="doc-h3">Static tokens</h3><p class="doc-p">These do not change between themes.</p>%s'
            '<h3 class="doc-h3">Color tokens</h3><p class="doc-p">Every semantic token with its dark and light value. These change per theme.</p>%s%s'
            % (files, table(["Group", "Count", "Examples"], [[a, b, inline_md(c)] for a, b, c in static_rows]), flt, ref))
    P.section("tokens", "Tokens and files", body, lead="Everything Hali ships, and every value in it.")


def versioning_section():
    rows = [
        ["Major", "2.0.0", "Removing or renaming a token, class or icon. Changing a layout metric or required markup. Weakening a contrast guarantee. Changing the default theme."],
        ["Minor", "1.1.0", "New tokens, components, variants and icons. Deprecations. Color refinements that keep every role and every contrast check passing."],
        ["Patch", "1.0.1", "Fixing a contrast miss or a rendering bug. Documentation fixes. Nothing that adds API surface."],
    ]
    body = ('<p class="doc-p">Hali follows Semantic Versioning, with one version for the whole system. Tokens, CSS, icons, script and docs always ship together. The public API is token names and their guarantees, class names and markup, icon ids, layout metrics and the theme attributes. Specific color values are not API: roles and contrast guarantees are.</p>%s'
            '<h3 class="doc-h3">Deprecation</h3>%s<p class="doc-p h-text-subtle">The full policy, release checklist and changelog conventions are in <code class="h-code">docs/VERSIONING.md</code>.</p>'
            % (table(["Change", "Example", "What qualifies"], [[a, "<code class=\"h-code\">%s</code>" % b, c] for a, b, c in rows]),
               ul(["Announce it in the release that adds the replacement, under **Deprecated**.",
                   "Keep it working for at least one full minor release.",
                   "Remove it only in the next major release, under **Removed**."])))
    P.section("versioning", "Versioning", body, lead="Semantic Versioning for a design language.")


def parse_changelog():
    text = read("CHANGELOG.md")
    blocks = re.split(r"(?m)^## ", text)[1:]
    out = []
    seen_release = False
    for block in blocks:
        lines = block.splitlines()
        head = re.match(r"\[(.+?)\](?: - (\S+))?", lines[0])
        version, date = head.group(1), head.group(2)
        badge = ""
        if version != "Unreleased" and not seen_release:
            badge = '<span class="h-lozenge h-is-brand">Latest</span>'
            seen_release = True
        title = version if version == "Unreleased" else "Version %s" % version
        date_html = '<span class="h-body-sm h-text-subtle" style="font-weight:400">%s</span>' % date if date else ""
        html_parts = ['<div class="doc-release"><h3>%s %s %s</h3>' % (esc(title), badge, date_html)]
        items = []
        para = []
        in_list = False

        def flush_para():
            if para:
                html_parts.append('<p class="doc-p">%s</p>' % inline_md(" ".join(para)))
                del para[:]

        def flush_list():
            nonlocal in_list
            if in_list:
                html_parts.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline_md(i) for i in items))
                del items[:]
                in_list = False

        for line in lines[1:]:
            if re.match(r"^\[.+\]: ", line):
                continue
            if line.startswith("### "):
                flush_para(); flush_list()
                html_parts.append("<h4>%s</h4>" % esc(line[4:]))
            elif line.startswith("- "):
                flush_para()
                in_list = True
                items.append(line[2:])
            elif line.startswith("  ") and in_list and items:
                items[-1] += " " + line.strip()
            elif line.strip() == "":
                flush_para()
            else:
                flush_list()
                para.append(line.strip())
        flush_para(); flush_list()
        html_parts.append("</div>")
        out.append("".join(html_parts))
    return "".join(out)


def changelog_section():
    P.section("changelog", "Changelog", parse_changelog(),
              lead="Every notable change, newest first. Follows Keep a Changelog.")


def roadmap_section():
    items = [
        "**Date picker and calendar.** Needs careful keyboard and screen reader work, so it waits for its own release.",
        "**Combobox and multi select.** The most requested missing input.",
        "**Tree view and stepper.**",
        "**Chart components.** The data visualization palette is ready. The components are not.",
        "**Density modes.** Compact and comfortable variants of control sizes and table rows.",
        "**A Figma library** generated from the same tokens.",
    ]
    body = ('<p class="doc-p">These are directions, not promises. Each would arrive in a minor release.</p>%s'
            '<h3 class="doc-h3">Contributing</h3><p class="doc-p">Propose a component with a short issue that answers four questions: what job does it do that nothing does today, which native element does it build on, what states does it have, and how does it behave at 320px, with a keyboard, and with a screen reader. Every pull request runs the build, which fails on any contrast miss or version mismatch. See <code class="h-code">CONTRIBUTING.md</code>.</p>' % ul(items))
    P.section("roadmap", "Roadmap and contributing", body, lead="What is next, and how to help.")


# ---------------------------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------------------------

def build():
    P.group("Start")
    overview()
    getting_started()
    principles()
    P.group("Foundations")
    color()
    typography()
    spacing()
    layout()
    shape()
    elevation()
    motion()
    iconography()
    dataviz()
    accessibility()
    content()
    P.group("Components")
    components_intro()
    component_sections()
    pattern_sections()
    P.group("Resources")
    tokens_section()
    versioning_section()
    changelog_section()
    roadmap_section()

    topbar = """
<header class="h-topbar doc-topbar">
  <button class="h-button h-button--subtle h-button--icon doc-menu-btn" type="button" aria-label="Menu" aria-expanded="false">%(menu)s</button>
  <a class="h-topbar__brand" href="#overview">%(mark)s Hali <span class="h-lozenge h-is-brand">%(v)s</span></a>
  <span class="doc-topbar__tag">Design language</span>
  <div class="h-topbar__actions" style="gap:12px">
    <div class="h-segmented" role="group" aria-label="Theme">
      <button type="button" data-theme-set="dark" aria-pressed="true">%(moon)s<span class="doc-segmented-label">Dark</span></button>
      <button type="button" data-theme-set="light" aria-pressed="false">%(sun)s<span class="doc-segmented-label">Light</span></button>
    </div>
    <label class="h-switch"><input type="checkbox" role="switch" data-contrast-toggle><span>High contrast</span></label>
  </div>
</header>""" % {"menu": I("menu"), "mark": C.MARK("h-icon--lg h-icon--brand"), "v": VERSION, "moon": I("moon", "h-icon--sm"), "sun": I("sun", "h-icon--sm")}

    footer = ('<footer class="doc-footer doc-wrap">Hali design language %s. Built from the files in this repository by '
              '<code class="h-code">scripts/build_site.py</code>. Colors are from the Nord palette by Arctic Ice Studio.</footer>' % VERSION)

    css = "\n".join(read(p) for p in ("tokens/hali-tokens.css", "css/hali.css")) + "\n" + A.DOC_CSS
    css += "\n.doc-dot { display:inline-block; width:14px; height:14px; margin-right:8px; border:1px solid var(--hali-border-strong); border-radius:4px; vertical-align:-2px; }\n"
    css += ".doc-section--component { padding-top: 56px; }\n.doc-section--component .doc-h3 { margin-top: 0; }\n"
    js = read("js/hali.js") + "\n" + A.DOC_JS

    page = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark light">
<title>Hali design language %(v)s</title>
<meta name="description" content="Hali is a dark first design language for web applications: Nord at its core, Atlassian structure, Material 3 tonal surfaces, readable by default.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap">
<script>%(head_js)s</script>
<style>
%(css)s
</style>
</head>
<body>
<a class="h-skip" href="#main">Skip to content</a>
%(sprite)s
%(topbar)s
<div class="doc-layout">
<nav class="doc-nav" aria-label="Documentation">%(nav)s</nav>
<main class="doc-main" id="main" tabindex="-1">
%(main)s
%(footer)s
</main>
</div>
<script>
%(js)s
</script>
</body>
</html>
""" % {"v": VERSION, "head_js": A.HEAD_JS, "css": css, "sprite": SPRITE, "topbar": topbar, "nav": P.nav_html(),
       "main": "\n".join(P.parts), "footer": footer, "js": js}

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("Wrote site/index.html (%d KB), %d sections" % (len(page.encode("utf-8")) // 1024, len(P.parts)))


if __name__ == "__main__":
    build()
