from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .config import settings

def _font(size, bold=False):
    p = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    try:
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()

def build_comic(story):
    panels = story["panels"]
    thumb_w, thumb_h = 900, 570
    margin, gap = 35, 25
    header = 150
    canvas = Image.new("RGB", (2*thumb_w+3*margin, header+3*thumb_h+4*margin), "white")
    d = ImageDraw.Draw(canvas)
    d.text((margin, 35), story["title"], fill="black", font=_font(55, True))
    d.text((margin, 100), story["subtitle"], fill="black", font=_font(25))
    for i, p in enumerate(panels):
        im = Image.open(settings.panels_dir / Path(p["image_url"]).name).convert("RGB")
        im.thumbnail((thumb_w, thumb_h))
        x = margin + (i % 2) * (thumb_w + gap)
        y = header + margin + (i // 2) * (thumb_h + gap)
        canvas.paste(im, (x, y))
    out = settings.exports_dir / "comic_preview.png"
    canvas.save(out)
    return f"/static/exports/{out.name}"
