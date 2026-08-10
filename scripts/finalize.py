#!/usr/bin/env python3
"""
finalize.py — post-processing local:
  1) cutouts transparentes de logo, sello, splashes e iconset
  2) favicon set (16/32/180 + .ico)
Se ejecuta con el venv de _scripts/.venv.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# --- cutout helpers ---
# Strategy: cream is the only palette color with L > ~78%.
# Everything meaningful (black ink, cadmium, cobalt, ochre, phthalo) has L <= 55%.
# We threshold on luminance so paper texture variations of cream all get zeroed
# without eating any real content.
def cutout_cream(img: Image.Image, l_full: int = 205, l_edge: int = 175) -> Image.Image:
    """
    - luminance >= l_full → fully transparent
    - l_edge < luminance < l_full → feathered (partial alpha)
    - luminance <= l_edge → opaque
    Uses ITU-R BT.601 luminance (approx of perceptual lightness).
    """
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    span = max(l_full - l_edge, 1)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            # BT.601 luma
            y_lum = (299 * r + 587 * g + 114 * b) // 1000
            if y_lum >= l_full:
                px[x, y] = (r, g, b, 0)
            elif y_lum > l_edge:
                # linear feather: brighter pixel → more transparent
                t = (y_lum - l_edge) / span
                new_a = int(a * (1.0 - t))
                px[x, y] = (r, g, b, new_a)
            # else: opaque
    return img

def cutout_file(src: Path, dst: Path, l_full: int = 205, l_edge: int = 175) -> None:
    img = Image.open(src)
    out = cutout_cream(img, l_full=l_full, l_edge=l_edge)
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, "PNG", optimize=True)
    # quick alpha report
    a = out.split()[3]
    total = a.width * a.height
    zero = sum(1 for p in a.getdata() if p == 0)
    print(f"  ok  {dst.relative_to(ROOT)}  ({100*zero/total:.0f}% transparent)")

# --- favicon helpers ---
def make_favicons(logo_src: Path, out_dir: Path) -> None:
    """
    Create favicon-16, favicon-32, apple-touch-icon-180, favicon.ico
    Sources from the CUTOUT logo (transparent bg) so the tab icon looks right on any browser theme.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(logo_src).convert("RGBA")

    # Crop tight around visible pixels so the wordmark fills the favicon
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # Add a small padding so the wordmark doesn't kiss the edge
    w, h = img.size
    pad = max(w, h) // 20
    padded = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    padded.paste(img, (pad, pad), img)
    img = padded

    for size in (16, 32, 180):
        thumb = img.copy()
        thumb.thumbnail((size, size), Image.LANCZOS)
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        off = ((size - thumb.width) // 2, (size - thumb.height) // 2)
        canvas.paste(thumb, off, thumb)
        name = "apple-touch-icon.png" if size == 180 else f"favicon-{size}.png"
        canvas.save(out_dir / name, "PNG", optimize=True)
        print(f"  ok  favicon/{name}")

    # .ico bundling 16 & 32
    ico_src = img.copy()
    ico_src.save(out_dir / "favicon.ico", sizes=[(16, 16), (32, 32)])
    print(f"  ok  favicon/favicon.ico")


def main() -> None:
    print("[1/2] cutouts")
    cutout_pairs = [
        (ROOT / "logo" / "logo_A_firma_cream.png",  ROOT / "logo" / "logo_A_firma_transparent_final.png"),
        (ROOT / "extras" / "sello_hecho_a_mano.png", ROOT / "extras" / "sello_hecho_a_mano_alpha.png"),
        (ROOT / "extras" / "iconset_media.png",      ROOT / "extras" / "iconset_media_alpha.png"),
    ] + [
        (ROOT / "extras" / f"splash_{s}.png", ROOT / "extras" / f"splash_{s}_alpha.png")
        for s in ("colores", "acuarela", "oleo", "pastel", "charcoal")
    ]
    for src, dst in cutout_pairs:
        if not src.exists():
            print(f"  SKIP  {src.name} missing")
            continue
        cutout_file(src, dst)

    print("\n[2/3] favicon set")
    logo_cutout = ROOT / "logo" / "logo_A_firma_transparent_final.png"
    make_favicons(logo_cutout, ROOT / "favicon")

    print("\n[3/3] logo dark-mode variant (cream on transparent)")
    src = Image.open(logo_cutout).convert("RGBA")
    w, h = src.size
    px = src.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            # if it's the cadmium dot (very orange) leave it as is
            if r > 200 and g < 140 and b < 80:
                continue
            # everything else = wordmark ink → paint it cream
            px[x, y] = (0xF4, 0xEB, 0xDD, a)
    dst = ROOT / "logo" / "logo_A_firma_cream_on_dark.png"
    src.save(dst, "PNG", optimize=True)
    print(f"  ok  {dst.relative_to(ROOT)}")

    print("\ndone")


if __name__ == "__main__":
    main()
