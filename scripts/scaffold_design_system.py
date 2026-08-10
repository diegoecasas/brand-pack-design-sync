#!/usr/bin/env python3
"""
scaffold_design_system.py — emit a Claude Design system package skeleton from a brand spec.

Generates the deterministic parts (tokens, styles.css, guideline cards, SKILL.md,
readme, folder tree) so you only hand-author the brand-specific components.

  python3 scaffold_design_system.py brand.json --out ~/Desktop/acme-design-system

Brand spec (JSON):
{
  "brand":        "Mascotearte",
  "slug":         "mascotearte",
  "system_name":  "Estudio Alegre",
  "lang":         "es",
  "blurb":        "Two-to-three sentences in the brand voice.",
  "colors": [
    {"var": "lienzo",  "name": "Lienzo Crudo",     "hex": "#F4EBDD", "role": "ground"},
    {"var": "tinta",   "name": "Tinta Nocturna",   "hex": "#141215", "role": "ink"},
    {"var": "cadmio",  "name": "Cadmio Vivo",      "hex": "#F26A1F", "role": "accent"},
    {"var": "cobalto", "name": "Cobalto Estudio",  "hex": "#1E4FCC", "role": "accent-2"},
    {"var": "ocre",    "name": "Ocre Antiguo",     "hex": "#C48A3B", "role": "warm"},
    {"var": "ftalo",   "name": "Verde Ftalo",      "hex": "#2A6E5A", "role": "calm"}
  ],
  "fonts": {
    "display": {"family": "Fraunces", "stack": "'Fraunces', serif",   "google": "Fraunces:opsz,wght@9..144,500;9..144,700"},
    "body":    {"family": "Inter",    "stack": "'Inter', sans-serif", "google": "Inter:wght@400;500;600"}
  },
  "tone_words": ["alegre", "físico", "premium", "confiable", "cálido"],
  "dos":   ["Show the process, not just the result."],
  "donts": ["Never use pure #FFFFFF — always the cream ground."]
}

Roles: exactly one "ground" and one "ink" are required; the rest are free-form.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------- helpers

def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_str(h: str) -> str:
    r, g, b = hex_to_rgb(h)
    return f"{r} {g} {b}"


def relative_luminance(h: str) -> float:
    def chan(c: int) -> float:
        s = c / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = hex_to_rgb(h)
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast_ratio(a: str, b: str) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def pick(colors: list[dict], role: str) -> dict | None:
    return next((c for c in colors if c.get("role") == role), None)


def card_header(group: str, name: str, subtitle: str, w: int, h: int) -> str:
    return (f'<!-- @dsCard group="{group}" viewport="{w}x{h}" '
            f'name="{name}" subtitle="{subtitle}" -->')


def card_doc(header: str, lang: str, body: str, extra_css: str = "", depth: int = 1) -> str:
    up = "../" * depth
    return f"""{header}
<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8">
<link rel="stylesheet" href="{up}styles.css">
<style>body{{margin:0;padding:18px 20px;background:var(--ground);font-family:var(--font-body)}}
{extra_css}</style>
</head><body>
{body}
</body></html>
"""


# ---------------------------------------------------------------- tokens

def tokens_colors(spec: dict) -> str:
    colors = spec["colors"]
    ground = pick(colors, "ground") or colors[0]
    ink = pick(colors, "ink") or colors[-1]

    lines = [
        "/* Raw palette — the only colors that exist in this brand. */",
        ":root {",
    ]
    for c in colors:
        lines.append(f"  --{c['var']}: {c['hex']};")
    lines.append("")
    lines.append("  /* RGB channels, for color-mix and alpha composition */")
    for c in colors:
        lines.append(f"  --{c['var']}-rgb: {rgb_str(c['hex'])};")

    lines += ["", "  /* Alpha ramps derived from ink — borders, scrims, hairlines */"]
    for a in (6, 12, 24, 40, 64):
        lines.append(f"  --{ink['var']}-a{a}: rgb(var(--{ink['var']}-rgb) / {a/100:.2f});")

    lines += [
        "",
        "  /* Ground aliases — what a surface stands on */",
        f"  --ground: var(--{ground['var']});",
        f"  --ground-ink: var(--{ink['var']});",
        "",
        "  /* Semantic text */",
        f"  --text-strong: var(--{ink['var']});",
        f"  --text-muted: rgb(var(--{ink['var']}-rgb) / 0.64);",
        f"  --text-faint: rgb(var(--{ink['var']}-rgb) / 0.40);",
        f"  --text-inverse: var(--{ground['var']});",
        "",
        "  /* Semantic surfaces */",
        f"  --surface-page: var(--{ground['var']});",
        f"  --surface-card: color-mix(in srgb, var(--{ground['var']}) 94%, white);",
        f"  --surface-sunken: color-mix(in srgb, var(--{ground['var']}) 92%, var(--{ink['var']}));",
        f"  --border-hairline: var(--{ink['var']}-a12);",
        f"  --border-strong: var(--{ink['var']}-a24);",
        "}",
        "",
        "/* Ground switching: put data-ground=\"ink\" on a section and every",
        "   semantic var flips. Components never need a `dark` prop. */",
        '[data-ground="ink"] {',
        f"  --ground: var(--{ink['var']});",
        f"  --ground-ink: var(--{ground['var']});",
        f"  --text-strong: var(--{ground['var']});",
        f"  --text-muted: rgb(var(--{ground['var']}-rgb) / 0.72);",
        f"  --text-faint: rgb(var(--{ground['var']}-rgb) / 0.48);",
        f"  --text-inverse: var(--{ink['var']});",
        f"  --surface-page: var(--{ink['var']});",
        f"  --surface-card: color-mix(in srgb, var(--{ink['var']}) 92%, white);",
        f"  --surface-sunken: color-mix(in srgb, var(--{ink['var']}) 96%, black);",
        f"  --border-hairline: rgb(var(--{ground['var']}-rgb) / 0.16);",
        f"  --border-strong: rgb(var(--{ground['var']}-rgb) / 0.32);",
        "}",
        "",
    ]
    return "\n".join(lines)


def tokens_fonts(spec: dict) -> str:
    f = spec["fonts"]
    fams = [v["google"] for v in f.values() if v.get("google")]
    imp = ""
    if fams:
        q = "&".join(f"family={x}" for x in fams)
        imp = f"@import url('https://fonts.googleapis.com/css2?{q}&display=swap');\n\n"
    return (imp + ":root {\n"
            f"  --font-display: {f['display']['stack']};\n"
            f"  --font-body: {f['body']['stack']};\n"
            "  --font-mono: ui-monospace, SFMono-Regular, Menlo, monospace;\n"
            "}\n")


TOKENS_TYPOGRAPHY = """:root {
  /* Composite type roles — use as `font: var(--text-body-role)` */
  --text-display-xl-role: 700 clamp(2.5rem, 6vw, 4.5rem)/1.03 var(--font-display);
  --text-display-role:    700 clamp(2rem, 4vw, 3rem)/1.08 var(--font-display);
  --text-title-role:      700 1.5rem/1.2 var(--font-display);
  --text-subtitle-role:   500 1.125rem/1.4 var(--font-body);
  --text-body-role:       400 1rem/1.6 var(--font-body);
  --text-small-role:      400 0.875rem/1.5 var(--font-body);
  --text-caption-role:    600 0.75rem/1.3 var(--font-body);
  --text-eyebrow-role:    600 0.6875rem/1.2 var(--font-body);

  --tracking-eyebrow: 0.12em;
  --tracking-display: -0.02em;
}
"""

TOKENS_SPACING = """:root {
  --space-3xs: 0.25rem;
  --space-2xs: 0.5rem;
  --space-xs:  0.75rem;
  --space-sm:  1rem;
  --space-md:  1.5rem;
  --space-lg:  2rem;
  --space-xl:  3rem;
  --space-2xl: 4rem;
  --space-3xl: 6rem;
  --space-4xl: 8rem;

  /* Layout rhythm */
  --gutter: clamp(1.25rem, 5vw, 4rem);
  --measure: 68ch;
  --container: 1200px;
  --section-y: clamp(3rem, 8vw, 6rem);
}
"""

TOKENS_RADIUS = """:root {
  --radius-xs: 4px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-xl: 32px;
  --radius-pill: 999px;
}
"""


def tokens_elevation(spec: dict) -> str:
    ink = pick(spec["colors"], "ink") or spec["colors"][-1]
    v = ink["var"]
    return (":root {\n"
            f"  --shadow-xs: 0 1px 2px rgb(var(--{v}-rgb) / 0.06);\n"
            f"  --shadow-sm: 0 2px 8px rgb(var(--{v}-rgb) / 0.08);\n"
            f"  --shadow-md: 0 8px 24px rgb(var(--{v}-rgb) / 0.10);\n"
            f"  --shadow-lg: 0 16px 48px rgb(var(--{v}-rgb) / 0.14);\n"
            f"  --shadow-frame: 0 24px 64px rgb(var(--{v}-rgb) / 0.18);\n"
            "}\n")


TOKENS_MOTION = """:root {
  --dur-instant: 80ms;
  --dur-fast:   140ms;
  --dur-base:   220ms;
  --dur-slow:   400ms;
  --dur-scene:  800ms;

  --ease-out:  cubic-bezier(0.22, 1, 0.36, 1);
  --ease-in:   cubic-bezier(0.55, 0, 1, 0.45);
  --ease-both: cubic-bezier(0.65, 0, 0.35, 1);

  --press-scale: 0.97;
}

@media (prefers-reduced-motion: reduce) {
  :root { --dur-fast: 0ms; --dur-base: 0ms; --dur-slow: 0ms; --dur-scene: 0ms; }
}
"""

TOKENS_TEXTURE = """:root {
  /* Point these at the real files once the brand pack has generated them.
     Kept as vars so a section can swap ground texture with one property. */
  --texture-primary: url('assets/textures/texture-primary.png');
  --texture-secondary: url('assets/textures/texture-secondary.png');
  --texture-grain: url('assets/textures/grain-overlay.png');

  --texture-tile: 600px;
  --texture-opacity: 0.5;
  --grain-opacity: 0.35;
}
"""

TOKENS_BASE = """*, *::before, *::after { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; }

body {
  margin: 0;
  background: var(--surface-page);
  color: var(--text-strong);
  font: var(--text-body-role);
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4 { margin: 0; font-family: var(--font-display); letter-spacing: var(--tracking-display); }
p { margin: 0; }
img, video { max-width: 100%; display: block; }

:where(a) { color: inherit; }

:where(:focus-visible) {
  outline: 2px solid var(--accent, var(--text-strong));
  outline-offset: 2px;
}
"""

STYLES_CSS = """/* Single entry point. Every card and component links only this file. */
@import url('tokens/fonts.css');
@import url('tokens/colors.css');
@import url('tokens/typography.css');
@import url('tokens/spacing.css');
@import url('tokens/radius.css');
@import url('tokens/elevation.css');
@import url('tokens/motion.css');
@import url('tokens/texture.css');
@import url('tokens/base.css');
"""


# ---------------------------------------------------------------- cards

def card_pigments(spec: dict) -> str:
    colors = spec["colors"]
    n = len(colors)
    cells = "".join(
        f'<div class="s"><div class="chip" style="background:{c["hex"]}"></div>'
        f'<div class="meta"><span class="n">{c["name"]}</span>'
        f'<span class="h">{c["hex"].upper()}</span>'
        f'<span class="r">--{c["var"]}</span></div></div>'
        for c in colors
    )
    # Long color names wrap to a second line; size the card so nothing clips.
    # ~7.4px/char is realistic for 12px semibold. Over-reserving is harmless, clipping is not.
    longest = max(len(c["name"]) for c in colors)
    col_w = 700 / n
    name_lines = 2 if longest * 7.4 > col_w - 16 else 1
    # Box math, verified by measuring scrollHeight in a browser:
    #   body padding 36 + chip 56 + meta padding 14 + hex 16.3 + token 15 + borders 2 = 139.3
    #   + name block at 1.3em on 12px = 15.6 per line
    height = round(139.3 + name_lines * 15.6) + 4  # +4 slack

    css = (f".sw{{display:grid;grid-template-columns:repeat({n},1fr);gap:10px}}"
           ".s{border-radius:var(--radius-sm);overflow:hidden;border:1px solid var(--border-hairline);"
           "display:flex;flex-direction:column}"
           ".chip{height:56px;flex:none}"
           ".meta{padding:7px 8px;background:var(--surface-card);flex:1}"
           ".n{font:var(--text-caption-role);color:var(--text-strong);display:block;"
           f"min-height:calc({name_lines} * 1.3em)}}"
           ".h{font:11px/1.3 var(--font-mono);color:var(--text-muted);display:block;margin-top:2px}"
           ".r{font:10px/1.3 var(--font-mono);color:var(--text-faint);display:block;margin-top:2px}")
    hdr = card_header("Colors", f"The {n} colors",
                      f"The entire palette. Nothing outside these {n}.", 700, height)
    return card_doc(hdr, spec.get("lang", "en"), f'<div class="sw">{cells}</div>', css)


def card_grounds(spec: dict) -> str:
    ground = pick(spec["colors"], "ground") or spec["colors"][0]
    ink = pick(spec["colors"], "ink") or spec["colors"][-1]
    body = (
        '<div class="g">'
        f'<section class="pane"><span class="eyebrow">default</span>'
        f'<h3>Aa</h3><p>Body copy on the {ground["name"]} ground.</p>'
        '<code>--ground</code></section>'
        f'<section class="pane" data-ground="ink"><span class="eyebrow">data-ground="ink"</span>'
        f'<h3>Aa</h3><p>The same markup, inverted automatically.</p>'
        '<code>[data-ground="ink"]</code></section>'
        '</div>'
    )
    css = (".g{display:grid;grid-template-columns:1fr 1fr;gap:12px}"
           ".pane{background:var(--surface-page);color:var(--text-strong);"
           "border:1px solid var(--border-hairline);border-radius:var(--radius-md);padding:16px}"
           ".eyebrow{font:var(--text-eyebrow-role);letter-spacing:var(--tracking-eyebrow);"
           "text-transform:uppercase;color:var(--text-faint)}"
           "h3{font:var(--text-title-role);margin:6px 0 4px}"
           "p{font:var(--text-small-role);color:var(--text-muted)}"
           "code{font:11px/1.3 var(--font-mono);color:var(--text-faint);display:block;margin-top:10px}")
    hdr = card_header("Colors", "Grounds",
                      "One markup, two grounds. Components never need a dark variant.", 700, 200)
    return card_doc(hdr, spec.get("lang", "en"), body, css)


def card_semantic_text(spec: dict) -> str:
    rows = [("--text-strong", "Strong — headings and primary copy"),
            ("--text-muted", "Muted — secondary copy, captions"),
            ("--text-faint", "Faint — metadata, disabled")]
    body = '<div class="rows">' + "".join(
        f'<div class="row"><span style="color:var({v})">{label}</span>'
        f'<code>{v}</code></div>' for v, label in rows) + "</div>"
    css = (".rows{display:flex;flex-direction:column;gap:10px}"
           ".row{display:flex;justify-content:space-between;align-items:baseline;"
           "padding-bottom:8px;border-bottom:1px solid var(--border-hairline);font:var(--text-body-role)}"
           "code{font:11px/1.3 var(--font-mono);color:var(--text-faint)}")
    hdr = card_header("Colors", "Text roles", "Three weights of voice. Never more.", 700, 178)
    return card_doc(hdr, spec.get("lang", "en"), body, css)


def card_contrast(spec: dict) -> str:
    """Accessibility card — real computed ratios, no hand-waving."""
    ground = pick(spec["colors"], "ground") or spec["colors"][0]
    rows = []
    for c in spec["colors"]:
        if c["var"] == ground["var"]:
            continue
        ratio = contrast_ratio(c["hex"], ground["hex"])
        if ratio >= 7:
            verdict, cls = "AAA", "ok"
        elif ratio >= 4.5:
            verdict, cls = "AA", "ok"
        elif ratio >= 3:
            verdict, cls = "AA Large only", "warn"
        else:
            verdict, cls = "Decorative only", "bad"
        rows.append(
            f'<div class="row"><span class="dot" style="background:{c["hex"]}"></span>'
            f'<span class="nm">{c["name"]}</span>'
            f'<span class="ratio">{ratio:.1f}:1</span>'
            f'<span class="v {cls}">{verdict}</span></div>')
    body = (f'<p class="lead">Contrast against {ground["name"]} '
            f'<code>{ground["hex"].upper()}</code></p>'
            '<div class="rows">' + "".join(rows) + "</div>")
    css = (".lead{font:var(--text-caption-role);color:var(--text-muted);margin-bottom:10px}"
           ".lead code{font:11px var(--font-mono)}"
           ".rows{display:flex;flex-direction:column;gap:7px}"
           ".row{display:grid;grid-template-columns:16px 1fr auto auto;gap:10px;align-items:center;"
           "font:var(--text-small-role)}"
           ".dot{width:14px;height:14px;border-radius:4px;border:1px solid var(--border-hairline)}"
           ".ratio{font:11px var(--font-mono);color:var(--text-muted)}"
           ".v{font:var(--text-caption-role);padding:2px 7px;border-radius:var(--radius-pill)}"
           ".ok{background:var(--border-hairline);color:var(--text-strong)}"
           ".warn{background:var(--border-strong);color:var(--text-strong)}"
           ".bad{background:var(--border-strong);color:var(--text-muted)}")
    hdr = card_header("Colors", "Contrast", "Which colors may carry text, and at what size.",
                      700, 62 + len(rows) * 27)
    return card_doc(hdr, spec.get("lang", "en"), body, css)


def card_type_scale(spec: dict) -> str:
    roles = [("--text-display-xl-role", "Display XL", "Hero headline"),
             ("--text-display-role", "Display", "Section headline"),
             ("--text-title-role", "Title", "Card title"),
             ("--text-subtitle-role", "Subtitle", "Lead paragraph"),
             ("--text-body-role", "Body", "Running copy"),
             ("--text-small-role", "Small", "Secondary copy"),
             ("--text-caption-role", "Caption", "Labels"),
             ("--text-eyebrow-role", "Eyebrow", "Section kicker")]
    body = '<div class="rows">' + "".join(
        f'<div class="row"><span class="spec" style="font:var({v})">{label}</span>'
        f'<span class="meta"><code>{v}</code> · {use}</span></div>'
        for v, label, use in roles) + "</div>"
    css = (".rows{display:flex;flex-direction:column;gap:12px}"
           ".row{display:flex;justify-content:space-between;align-items:baseline;gap:20px;"
           "padding-bottom:10px;border-bottom:1px solid var(--border-hairline)}"
           ".spec{color:var(--text-strong);white-space:nowrap}"
           ".meta{font:var(--text-caption-role);color:var(--text-faint);text-align:right;white-space:nowrap}"
           ".meta code{font:10px var(--font-mono)}")
    hdr = card_header("Type", "Type scale", "Eight roles. Compose with `font: var(--…)`.", 700, 440)
    return card_doc(hdr, spec.get("lang", "en"), body, css)


def card_type_pairing(spec: dict) -> str:
    f = spec["fonts"]
    body = (
        f'<div class="pair"><div class="col"><span class="eyebrow">Display</span>'
        f'<p class="big">{f["display"]["family"]}</p>'
        f'<p class="note">Headlines, numbers, anything that should feel authored.</p></div>'
        f'<div class="col"><span class="eyebrow">Body</span>'
        f'<p class="big body">{f["body"]["family"]}</p>'
        f'<p class="note">UI, running copy, labels. Everything else.</p></div></div>'
    )
    css = (".pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}"
           ".eyebrow{font:var(--text-eyebrow-role);letter-spacing:var(--tracking-eyebrow);"
           "text-transform:uppercase;color:var(--text-faint)}"
           ".big{font:var(--text-display-role);margin:6px 0 8px}"
           ".big.body{font-family:var(--font-body)}"
           ".note{font:var(--text-small-role);color:var(--text-muted)}")
    hdr = card_header("Type", "Pairing",
                      f"{f['display']['family']} for voice, {f['body']['family']} for everything else.",
                      700, 175)
    return card_doc(hdr, spec.get("lang", "en"), body, css)


def card_spacing(spec: dict) -> str:
    steps = [("3xs", "0.25"), ("2xs", "0.5"), ("xs", "0.75"), ("sm", "1"),
             ("md", "1.5"), ("lg", "2"), ("xl", "3"), ("2xl", "4"), ("3xl", "6"), ("4xl", "8")]
    body = '<div class="rows">' + "".join(
        f'<div class="row"><code>--space-{k}</code>'
        f'<div class="bar" style="width:calc(var(--space-{k}) * 3)"></div>'
        f'<span class="v">{v}rem</span></div>' for k, v in steps) + "</div>"
    css = (".rows{display:flex;flex-direction:column;gap:6px}"
           ".row{display:grid;grid-template-columns:96px 1fr 56px;gap:12px;align-items:center}"
           "code{font:10px var(--font-mono);color:var(--text-muted)}"
           ".bar{height:12px;background:var(--accent, var(--text-strong));border-radius:var(--radius-xs);opacity:.85}"
           ".v{font:10px var(--font-mono);color:var(--text-faint);text-align:right}")
    hdr = card_header("Spacing", "Scale", "A 4px-rooted ramp. Do not invent values between steps.",
                      700, 40 + len(steps) * 18)
    return card_doc(hdr, spec.get("lang", "en"), body, css)


def card_radius(spec: dict) -> str:
    steps = ["xs", "sm", "md", "lg", "xl", "pill"]
    body = '<div class="row">' + "".join(
        f'<div class="item"><div class="box" style="border-radius:var(--radius-{k})"></div>'
        f'<code>--radius-{k}</code></div>' for k in steps) + "</div>"
    css = (".row{display:flex;gap:16px;align-items:flex-end}"
           ".item{text-align:center}"
           ".box{width:72px;height:56px;background:var(--surface-sunken);"
           "border:1px solid var(--border-strong);margin-bottom:6px}"
           "code{font:10px var(--font-mono);color:var(--text-muted)}")
    hdr = card_header("Radius", "Corners", "Six radii. Pill is for actions only.", 700, 140)
    return card_doc(hdr, spec.get("lang", "en"), body, css)


def card_elevation(spec: dict) -> str:
    steps = ["xs", "sm", "md", "lg", "frame"]
    body = '<div class="row">' + "".join(
        f'<div class="item"><div class="box" style="box-shadow:var(--shadow-{k})"></div>'
        f'<code>--shadow-{k}</code></div>' for k in steps) + "</div>"
    css = (".row{display:flex;gap:24px;align-items:center;padding:12px 4px}"
           ".item{text-align:center}"
           ".box{width:84px;height:60px;background:var(--surface-card);"
           "border-radius:var(--radius-md);margin-bottom:10px}"
           "code{font:10px var(--font-mono);color:var(--text-muted)}")
    hdr = card_header("Elevation", "Shadows", "Soft and warm. Never a hard black drop.", 700, 172)
    return card_doc(hdr, spec.get("lang", "en"), body, css)


def card_motion(spec: dict) -> str:
    body = (
        '<div class="rows">'
        '<div class="row"><code>--dur-fast · 140ms</code><div class="t"><i style="animation-duration:140ms"></i></div></div>'
        '<div class="row"><code>--dur-base · 220ms</code><div class="t"><i style="animation-duration:220ms"></i></div></div>'
        '<div class="row"><code>--dur-slow · 400ms</code><div class="t"><i style="animation-duration:400ms"></i></div></div>'
        '</div><p class="note">All easing is <code>--ease-out</code> unless something is leaving. '
        'Press shrinks to <code>--press-scale</code>. No bounce, ever.</p>'
    )
    css = (".rows{display:flex;flex-direction:column;gap:10px}"
           ".row{display:grid;grid-template-columns:180px 1fr;gap:14px;align-items:center}"
           "code{font:10px var(--font-mono);color:var(--text-muted)}"
           ".t{height:10px;background:var(--surface-sunken);border-radius:var(--radius-pill);overflow:hidden}"
           ".t i{display:block;height:100%;width:40%;border-radius:var(--radius-pill);"
           "background:var(--accent, var(--text-strong));"
           "animation-name:slide;animation-iteration-count:infinite;"
           "animation-timing-function:var(--ease-both);animation-direction:alternate}"
           "@keyframes slide{from{transform:translateX(0)}to{transform:translateX(150%)}}"
           ".note{font:var(--text-small-role);color:var(--text-muted);margin-top:14px}"
           ".note code{font:10px var(--font-mono)}")
    hdr = card_header("Motion", "Durations", "Three speeds. Everything eases out.", 700, 150)
    return card_doc(hdr, spec.get("lang", "en"), body, css)


# ---------------------------------------------------------------- docs

def skill_md(spec: dict) -> str:
    return f"""---
name: {spec['slug']}-design
description: Use this skill to generate well-branded interfaces and assets for {spec['brand']}, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.
If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets
out and create static HTML files for the user to view. If working on production code,
you can copy assets and read the rules here to become an expert in designing with this
brand. If the user invokes this skill without any other guidance, ask them what they
want to build or design, ask some questions, and act as an expert designer who outputs
HTML artifacts _or_ production code, depending on the need.
"""


def readme_md(spec: dict) -> str:
    colors = spec["colors"]
    rows = "\n".join(
        f"| {c['name']} | `{c['hex'].upper()}` | `--{c['var']}` | {c.get('role','—')} |"
        for c in colors)
    dos = "\n".join(f"- {d}" for d in spec.get("dos", [])) or "- _(fill in)_"
    donts = "\n".join(f"- {d}" for d in spec.get("donts", [])) or "- _(fill in)_"
    tone = " · ".join(spec.get("tone_words", [])) or "_(fill in)_"
    return f"""# {spec['brand']} — {spec.get('system_name', 'Design System')}

{spec.get('blurb', '')}

## Palette

| Name | Hex | Token | Role |
|---|---|---|---|
{rows}

Every color in the system is one of these. There is no seventh color.

## Type

- **Display** — {spec['fonts']['display']['family']} · `var(--font-display)`
- **Body** — {spec['fonts']['body']['family']} · `var(--font-body)`

Compose with the role shorthands: `font: var(--text-body-role)`.

## Tone

{tone}

## Do

{dos}

## Don't

{donts}

## Structure

```
styles.css              single entry point — link this and nothing else
tokens/                 the source of truth for every value
guidelines/*.card.html  the visible documentation cards
components/             .jsx + .d.ts + .prompt.md per component
assets/                 logo, photography, textures, motion
```

## Grounds

Sections carry their own ground. Put `data-ground="ink"` on a section and every
semantic token flips — text, surfaces, borders. Components read the ground they
stand on, so none of them need a `dark` prop.

```html
<section data-ground="ink">
  <!-- same markup, inverted automatically -->
</section>
```
"""


def thumbnail_html(spec: dict) -> str:
    ground = pick(spec["colors"], "ground") or spec["colors"][0]
    accent = pick(spec["colors"], "accent") or spec["colors"][2 % len(spec["colors"])]
    ink = pick(spec["colors"], "ink") or spec["colors"][-1]
    return f"""<!DOCTYPE html><html lang="{spec.get('lang','en')}"><head><meta charset="utf-8">
<link rel="stylesheet" href="styles.css">
<style>
body{{margin:0;height:100vh;display:grid;place-items:center;background:{ground['hex']}}}
.mark{{font:700 clamp(28px,7vw,64px)/1 var(--font-display);color:{ink['hex']};
letter-spacing:var(--tracking-display)}}
.dot{{display:inline-block;width:.22em;height:.22em;border-radius:50%;
background:{accent['hex']};margin-left:.1em;vertical-align:baseline}}
</style></head><body>
<div class="mark">{spec['brand']}<span class="dot"></span></div>
</body></html>
"""


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold a Claude Design system package")
    ap.add_argument("spec", help="path to brand spec JSON")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())

    for key in ("brand", "slug", "colors", "fonts"):
        if key not in spec:
            print(f"ERROR: spec is missing required key: {key}", file=sys.stderr)
            return 2
    if not pick(spec["colors"], "ground") or not pick(spec["colors"], "ink"):
        print('ERROR: colors must include exactly one role:"ground" and one role:"ink"',
              file=sys.stderr)
        return 2

    out = Path(args.out).expanduser()

    files: dict[str, str] = {
        "styles.css": STYLES_CSS,
        "SKILL.md": skill_md(spec),
        "readme.md": readme_md(spec),
        "thumbnail.html": thumbnail_html(spec),
        "tokens/colors.css": tokens_colors(spec),
        "tokens/fonts.css": tokens_fonts(spec),
        "tokens/typography.css": TOKENS_TYPOGRAPHY,
        "tokens/spacing.css": TOKENS_SPACING,
        "tokens/radius.css": TOKENS_RADIUS,
        "tokens/elevation.css": tokens_elevation(spec),
        "tokens/motion.css": TOKENS_MOTION,
        "tokens/texture.css": TOKENS_TEXTURE,
        "tokens/base.css": TOKENS_BASE,
        "guidelines/colors-pigments.card.html": card_pigments(spec),
        "guidelines/colors-grounds.card.html": card_grounds(spec),
        "guidelines/colors-semantic-text.card.html": card_semantic_text(spec),
        "guidelines/colors-contrast.card.html": card_contrast(spec),
        "guidelines/type-scale.card.html": card_type_scale(spec),
        "guidelines/type-pairing.card.html": card_type_pairing(spec),
        "guidelines/spacing-scale.card.html": card_spacing(spec),
        "guidelines/radius.card.html": card_radius(spec),
        "guidelines/elevation.card.html": card_elevation(spec),
        "guidelines/motion.card.html": card_motion(spec),
    }

    empty_dirs = [
        "components/core", "components/forms", "components/navigation",
        "components/feedback", "components/brand",
        "assets/logo", "assets/heroes", "assets/banner", "assets/action",
        "assets/detail", "assets/lifestyle", "assets/motion", "assets/textures",
        "assets/icons", "assets/extras", "assets/favicon",
        "templates", "ui_kits",
    ]

    written, skipped = 0, 0
    for rel, content in files.items():
        p = out / rel
        if p.exists() and not args.force:
            skipped += 1
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        written += 1
        print(f"  + {rel}")

    for d in empty_dirs:
        (out / d).mkdir(parents=True, exist_ok=True)

    print(f"\n{written} written, {skipped} skipped (use --force to overwrite)")
    print(f"→ {out}")
    print("\nNext:")
    print("  1. Copy the brand pack assets into assets/*")
    print("  2. Hand-author components/<group>/<Name>.{jsx,d.ts,prompt.md}")
    print("  3. Add a <group>.card.html gallery per component folder")
    print("  4. cd into the package, run `claude`, and type /design-sync yourself")
    return 0


if __name__ == "__main__":
    sys.exit(main())
