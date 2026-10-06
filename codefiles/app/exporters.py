from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from .config import settings

def build_pdf(story):
    out = settings.exports_dir / "comic.pdf"
    c = canvas.Canvas(str(out), pagesize=A4)
    W, H = A4
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, H-50, story["title"])
    y = H - 90
    for p in story["panels"]:
        img_path = settings.panels_dir / Path(p["image_url"]).name
        c.drawImage(ImageReader(str(img_path)), 40, y-220, width=W-80, height=210, preserveAspectRatio=True)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(40, y-240, f"Panel {p['panel_number']}: {p['caption'][:100]}")
        c.setFont("Helvetica", 10)
        c.drawString(40, y-255, p["dialogue"][:120])
        y -= 285
        if y < 100:
            c.showPage()
            y = H - 60
    c.save()
    return f"/static/exports/{out.name}"
