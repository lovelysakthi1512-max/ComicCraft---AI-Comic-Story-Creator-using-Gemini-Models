from pathlib import Path
import base64
import threading
import time
from PIL import Image, ImageDraw, ImageFont
from google import genai
from .config import settings

def _font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def _fallback_panel(number, caption, dialogue, style):
    w, h = 1200, 760
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    d.rectangle((25,25,w-25,h-25), outline="black", width=8)
    d.rectangle((45,45,w-45,150), fill="#1e293b")
    d.text((70,70), f"PANEL {number}  •  {style}", fill="white",
           font=_font(42, True))
    # Simple artistic fantasy scene
    d.ellipse((390,190,810,610), outline="#334155", width=10)
    d.polygon([(260,610),(600,230),(940,610)], outline="#475569", fill="#e2e8f0")
    d.rectangle((535,390,665,590), fill="#f8fafc", outline="#0f172a", width=8)
    d.ellipse((565,300,635,370), fill="#fde68a", outline="#0f172a", width=6)
    d.line((600,370,540,470), fill="#0f172a", width=12)
    d.line((600,370,660,470), fill="#0f172a", width=12)
    d.text((70,650), caption[:70], fill="#111827", font=_font(30, True))
    d.text((70,700), dialogue[:75], fill="#111827", font=_font(24))
    path = settings.panels_dir / f"panel_{number:02d}_fallback.png"
    img.save(path)
    return f"/static/panels/{path.name}"

def _real_image(prompt, number):
    if not settings.gemini_api_key:
        return None
    client = genai.Client(api_key=settings.gemini_api_key)
    result = [None]
    error = [None]

    def work():
        try:
            interaction = client.interactions.create(
                model=settings.image_model,
                input=prompt,
            )
            output = getattr(interaction, "output_image", None)
            if output and getattr(output, "data", None):
                raw = base64.b64decode(output.data)
                path = settings.panels_dir / f"panel_{number:02d}_ai.png"
                path.write_bytes(raw)
                result[0] = f"/static/panels/{path.name}"
            else:
                error[0] = RuntimeError("No image returned.")
        except Exception as exc:
            error[0] = exc

    thread = threading.Thread(target=work, daemon=True)
    thread.start()
    thread.join(settings.image_timeout)

    if thread.is_alive():
        print(f"[WARN] Panel {number}: image request timed out.")
        return None
    if error[0]:
        print(f"[WARN] Panel {number}: image unavailable: {error[0]}")
        return None
    return result[0]

def generate_image(prompt, number, caption="", dialogue="", style="Fantasy Comic"):
    print(f"[INFO] Panel {number}: trying Gemini image generation...")
    url = _real_image(prompt, number)
    if url:
        print(f"[SUCCESS] Real AI image generated for Panel {number}")
        return url
    print(f"[INFO] Panel {number}: using local artistic fallback.")
    return _fallback_panel(number, caption, dialogue, style)
