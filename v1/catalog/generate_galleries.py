#!/usr/bin/env python3
"""
VTT Gallery Generator
─────────────────────
Run from the same folder as VTT_Wholesale_Catalog_EU.html.

  python generate_galleries.py

On each run:
  - Scans subfolders named after UPC numbers (10–13 digits)
  - Wipes and fully rebuilds thumbs/ inside each
  - Generates a gallery.html per UPC folder (Camera CCM style)
  - Writes galleries.js listing every UPC that has a gallery

Product titles come from product_names.py — edit that file to
update names. No CSV or Excel files needed.

Supported image formats: .jpg .jpeg .png .gif .webp
PDF support: generates a styled filename tile (no Poppler needed)

Requirements:  pip install pillow
"""

import re, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── config ────────────────────────────────────────────────────────────────────
THUMB_MAX     = (400, 400)
THUMB_QUALITY = 85
GALLERIES_JS  = 'galleries.js'
UPC_RE        = re.compile(r'^\d{10,13}$')
IMG_EXTS      = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
PDF_EXT       = '.pdf'

# Camera CCM palette
INK     = (26,  24,  20)
SURFACE = (237, 233, 225)
FAINT   = (138, 132, 128)
ACCENT  = (200, 64,  26)

# ── product names ─────────────────────────────────────────────────────────────

def load_product_names() -> dict:
    """Load from product_names.py sitting next to this script."""
    p = Path('product_names.py')
    if not p.exists():
        print('  [warn] product_names.py not found — gallery titles will show UPC only.')
        return {}
    try:
        ns = {}
        exec(p.read_text(encoding='utf-8'), ns)
        names = ns.get('PRODUCT_NAMES', {})
        print(f'  Loaded {len(names)} product names from product_names.py')
        return names
    except Exception as e:
        print(f'  [warn] could not read product_names.py: {e}')
        return {}

# ── font helper ───────────────────────────────────────────────────────────────

def get_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/calibri.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

# ── thumbnail generation ──────────────────────────────────────────────────────

def make_image_thumb(src: Path, dst: Path) -> None:
    with Image.open(src) as img:
        img = img.convert('RGB')
        img.thumbnail(THUMB_MAX, Image.LANCZOS)
        img.save(dst, 'JPEG', quality=THUMB_QUALITY)


def make_pdf_thumb(src: Path, dst: Path) -> None:
    W, H    = THUMB_MAX
    img     = Image.new('RGB', (W, H), color=INK)
    draw    = ImageDraw.Draw(img)
    f_badge = get_font(16)
    f_name  = get_font(22)
    f_hint  = get_font(13)

    bw, bh = 56, 28
    bx, by = (W - bw) // 2, 56
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=4, fill=ACCENT)
    draw.text((W // 2, by + bh // 2), 'PDF', fill=(255, 255, 255),
              font=f_badge, anchor='mm')

    words = src.stem.replace('_', ' ').replace('-', ' ').split()
    lines, cur = [], ''
    for w in words:
        if len(cur) + len(w) + 1 <= 22:
            cur = (cur + ' ' + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    lines = lines[:5]

    y = (H - len(lines) * 32) // 2 + 8
    for line in lines:
        draw.text((W // 2, y), line, fill=SURFACE, font=f_name, anchor='mm')
        y += 32

    draw.text((W // 2, H - 36), 'click to open / download',
              fill=FAINT, font=f_hint, anchor='mm')
    img.save(dst, 'PNG')

# ── gallery page ──────────────────────────────────────────────────────────────

GALLERY_CSS = """
  :root {
    --paper: #f5f2ec; --surface: #ede9e1; --ink: #1a1814;
    --ink-soft: #4a4640; --ink-faint: #8a8480;
    --rule: #d8d4ca; --accent: #c8401a;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--paper); color: var(--ink);
    font-family: 'DM Sans', -apple-system, sans-serif; font-weight: 300;
  }
  .series-header {
    border-bottom: 1px solid var(--ink);
    padding: 18px 40px 14px; background: var(--paper); position: relative;
  }
  .series-header::before {
    content: ''; position: absolute; inset: 0 0 1px 0;
    background-image: linear-gradient(to right, var(--rule) 1px, transparent 1px);
    background-size: 80px 100%; opacity: 0.5; pointer-events: none;
  }
  .series-name {
    font-family: 'Arial Rounded MT Bold', 'Arial Black', sans-serif;
    font-size: 13px; letter-spacing: 0.18em; font-weight: 700;
  }
  .series-sub {
    font-family: 'DM Mono', monospace; font-size: 11px;
    color: var(--ink-faint); margin-top: 4px; letter-spacing: 0.05em;
  }
  main { max-width: 1200px; margin: 0 auto; padding: 56px 40px 80px; }
  .back-link {
    font-family: 'DM Mono', monospace; font-size: 11px;
    color: var(--accent); text-decoration: none; letter-spacing: 0.06em;
    text-transform: uppercase; display: inline-block; margin-bottom: 32px;
  }
  .back-link:hover { text-decoration: underline; }
  .eyebrow {
    font-family: 'DM Mono', monospace; font-size: 11px;
    letter-spacing: 0.18em; color: var(--ink-faint);
    text-transform: uppercase; margin-bottom: 14px;
  }
  h1 {
    font-family: 'Instrument Serif', serif; font-weight: 400;
    font-size: 42px; line-height: 1.1; margin: 0 0 8px;
    letter-spacing: -0.01em;
  }
  h1 em { font-style: italic; color: var(--accent); }
  .upc-sub {
    font-family: 'DM Mono', monospace; font-size: 12px;
    color: var(--ink-faint); margin-bottom: 40px; letter-spacing: 0.04em;
  }
  .rule { border: none; border-top: 1px solid var(--rule); margin-bottom: 40px; }
  .count { font-size: 13px; color: var(--ink-faint); margin-bottom: 32px; }
  .count strong { color: var(--ink); font-weight: 500; }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
  }
  .thumb-card {
    display: flex; flex-direction: column;
    background: var(--surface); border: 1px solid var(--rule);
    border-radius: 2px; overflow: hidden;
    text-decoration: none; color: inherit;
    transition: border-color 0.15s ease, transform 0.15s ease;
  }
  .thumb-card:hover { border-color: var(--accent); transform: translateY(-2px); }
  .thumb-img-wrap {
    aspect-ratio: 1 / 1; background: var(--paper);
    display: flex; align-items: center; justify-content: center; overflow: hidden;
  }
  .thumb-img-wrap img {
    max-width: 100%; max-height: 100%; object-fit: contain; display: block;
  }
  .thumb-name {
    font-family: 'DM Mono', monospace; font-size: 11px;
    color: var(--ink-faint); padding: 10px 12px;
    border-top: 1px solid var(--rule);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    letter-spacing: 0.02em;
  }
  footer {
    border-top: 1px solid var(--rule); margin-top: 64px; padding-top: 20px;
    font-family: 'DM Mono', monospace; font-size: 11px;
    color: var(--ink-faint); letter-spacing: 0.04em;
  }
  @media (max-width: 600px) {
    main { padding: 36px 20px 60px; }
    h1 { font-size: 28px; }
    .grid { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }
  }
"""


def gallery_html(upc: str, title: str, entries: list) -> str:
    cards = ''
    for thumb_rel, full_rel, display_name in entries:
        cards += f'''
      <a class="thumb-card" href="{full_rel}" target="_blank">
        <div class="thumb-img-wrap">
          <img src="{thumb_rel}" alt="{display_name}" loading="lazy">
        </div>
        <div class="thumb-name" title="{display_name}">{display_name}</div>
      </a>'''

    n    = len(entries)
    noun = 'file' if n == 1 else 'files'
    short = title if len(title) <= 55 else title[:52] + '…'
    # Strip any HTML entities for the page title
    short_clean = re.sub(r'&[a-z]+;', '', short)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Artwork — {upc} — VLADS TEST TARGET</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>
{GALLERY_CSS}
</style>
</head>
<body>
  <div class="series-header">
    <div class="series-name">VLADS TEST TARGET</div>
    <div class="series-sub">Artwork Gallery</div>
  </div>
  <main>
    <a class="back-link" href="../VTT_Wholesale_Catalog_EU.html">← Back to catalog</a>
    <div class="eyebrow">Artwork &amp; Press Images</div>
    <h1><em>Artwork</em> for<br>{short_clean}</h1>
    <div class="upc-sub">UPC {upc}</div>
    <hr class="rule">
    <p class="count"><strong>{n} {noun}</strong> available — click any thumbnail to open the full-size file.</p>
    <div class="grid">
{cards}
    </div>
    <footer>film4ever.info · VLADS TEST TARGET — generated by generate_galleries.py</footer>
  </main>
</body>
</html>'''

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    root = Path('.')
    print('VTT Gallery Generator')
    print('─' * 40)

    product_names   = load_product_names()
    galleries_found = []
    total_thumbs    = 0

    upc_dirs = sorted(
        [d for d in root.iterdir() if d.is_dir() and UPC_RE.match(d.name)],
        key=lambda d: d.name
    )

    if not upc_dirs:
        print('No UPC folders found. Create a folder named after a UPC')
        print('(e.g. 644637132545/) and place artwork inside it.')
        sys.exit(0)

    for upc_dir in upc_dirs:
        upc        = upc_dir.name
        thumbs_dir = upc_dir / 'thumbs'

        # Full wipe and rebuild
        if thumbs_dir.exists():
            shutil.rmtree(thumbs_dir)
        thumbs_dir.mkdir()

        sources = sorted(
            [f for f in upc_dir.iterdir()
             if f.is_file() and f.suffix.lower() in IMG_EXTS | {PDF_EXT}],
            key=lambda f: f.name.lower()
        )

        if not sources:
            print(f'  {upc}: no images found, skipping')
            continue

        entries = []
        for src in sources:
            is_pdf = src.suffix.lower() == PDF_EXT
            stem   = src.stem

            if is_pdf:
                thumb_name = f'{stem}_thumb.png'
                thumb_dst  = thumbs_dir / thumb_name
                try:
                    make_pdf_thumb(src, thumb_dst)
                except Exception as e:
                    print(f'    [warn] PDF tile failed for {src.name}: {e}')
                    continue
            else:
                thumb_name = f'{stem}_thumb.jpg'
                thumb_dst  = thumbs_dir / thumb_name
                try:
                    make_image_thumb(src, thumb_dst)
                except Exception as e:
                    print(f'    [warn] thumbnail failed for {src.name}: {e}')
                    continue

            entries.append((f'thumbs/{thumb_name}', src.name, src.name))

        if not entries:
            print(f'  {upc}: all thumbnails failed, skipping')
            continue

        title = product_names.get(upc, f'UPC {upc}')
        html  = gallery_html(upc, title, entries)
        (upc_dir / 'gallery.html').write_text(html, encoding='utf-8')

        total_thumbs += len(entries)
        galleries_found.append(upc)
        print(f'  {upc}: {len(entries)} file(s) → gallery.html written')

    # Write galleries.js
    upcs_js = ',\n  '.join(f'"{u}"' for u in galleries_found)
    js = (
        '// Auto-generated by generate_galleries.py — do not edit manually.\n'
        '// Re-run the script after adding or removing artwork.\n'
        f'const GALLERIES = new Set([\n  {upcs_js}\n]);\n'
    )
    Path(GALLERIES_JS).write_text(js, encoding='utf-8')

    print()
    print(f'Done. {len(galleries_found)} gallery/galleries, {total_thumbs} thumbnail(s) total.')
    print(f'Wrote {GALLERIES_JS}')


if __name__ == '__main__':
    main()
