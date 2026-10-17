"""Color math helpers for the Hali design language.

Everything here works on "#RRGGBB" strings and uses the WCAG 2.x relative luminance formula.
Lightness shifts happen in OKLCH so hue and chroma stay put: a Nord red stays a red when it is
lifted to meet a contrast target, instead of drifting toward gray.
"""

import math

WHITE = "#FFFFFF"
BLACK = "#000000"


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(c))) for c in rgb)


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _unlin(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def luminance(h):
    r, g, b = hex2rgb(h)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def mix(a, b, t):
    """Blend two colors in sRGB. t=0 gives a, t=1 gives b."""
    ra, rb = hex2rgb(a), hex2rgb(b)
    return rgb2hex(tuple(ra[i] + (rb[i] - ra[i]) * t for i in range(3)))


def rgba(h, alpha):
    r, g, b = hex2rgb(h)
    return "rgba(%d, %d, %d, %s)" % (r, g, b, ("%g" % alpha))


def worst(color, backgrounds):
    return min(contrast(color, bg) for bg in backgrounds)


# ---------------------------------------------------------------------------------------------
# OKLCH
# ---------------------------------------------------------------------------------------------

def hex_to_oklch(h):
    r, g, b = (_lin(c) for c in hex2rgb(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    lightness = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return lightness, math.hypot(a, bb), math.atan2(bb, a)


def _oklch_to_linear(lightness, chroma, hue):
    a = chroma * math.cos(hue)
    b = chroma * math.sin(hue)
    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bl = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return r, g, bl


def oklch_to_hex(lightness, chroma, hue):
    """Convert OKLCH to hex, reducing chroma if the color falls outside sRGB."""
    lightness = max(0.0, min(1.0, lightness))

    def inside(c):
        return all(-1e-4 <= x <= 1 + 1e-4 for x in _oklch_to_linear(lightness, c, hue))

    if not inside(chroma):
        lo, hi = 0.0, chroma
        for _ in range(32):
            mid = (lo + hi) / 2
            if inside(mid):
                lo = mid
            else:
                hi = mid
        chroma = lo
    r, g, b = _oklch_to_linear(lightness, chroma, hue)
    return rgb2hex((255 * _unlin(r), 255 * _unlin(g), 255 * _unlin(b)))


def shift_l(fg, direction, backgrounds, target):
    """Smallest OKLCH lightness shift of fg that reaches `target` contrast on every background.

    direction is +1 to lighten (dark themes) or -1 to darken (light themes). Hue and chroma are
    kept. If fg already passes it is returned unchanged.
    """
    if worst(fg, backgrounds) >= target:
        return fg
    l0, c0, h0 = hex_to_oklch(fg)
    end = 1.0 if direction > 0 else 0.0

    def at(t):
        return oklch_to_hex(l0 + (end - l0) * t, c0, h0)

    if worst(at(1.0), backgrounds) < target:
        return at(1.0)
    lo, hi = 0.0, 1.0
    for _ in range(48):
        mid = (lo + hi) / 2
        if worst(at(mid), backgrounds) >= target:
            hi = mid
        else:
            lo = mid
    return at(hi)


# ---------------------------------------------------------------------------------------------
# Neutral helpers (sRGB mixing is fine for low chroma Nord grays)
# ---------------------------------------------------------------------------------------------

def ensure(fg, toward, backgrounds, target):
    """Smallest mix of fg toward `toward` that reaches `target` contrast on every background."""
    if worst(fg, backgrounds) >= target:
        return fg
    if worst(toward, backgrounds) < target:
        return toward
    lo, hi = 0.0, 1.0
    for _ in range(48):
        mid = (lo + hi) / 2
        if worst(mix(fg, toward, mid), backgrounds) >= target:
            hi = mid
        else:
            lo = mid
    return mix(fg, toward, hi)


def soften(fg, toward, backgrounds, target):
    """Largest mix of fg toward `toward` that still holds `target` contrast on every background."""
    if worst(fg, backgrounds) < target:
        return fg
    lo, hi = 0.0, 1.0
    for _ in range(48):
        mid = (lo + hi) / 2
        if worst(mix(fg, toward, mid), backgrounds) >= target:
            lo = mid
        else:
            hi = mid
    return mix(fg, toward, lo)
