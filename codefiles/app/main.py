from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .config import settings
from .gemini import generate_story
from .image_generator import generate_image
from .comic_builder import build_comic
from .exporters import build_pdf

app = FastAPI(title="ComicCraft AI Comic Creator")
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
templates = Jinja2Templates(directory=str(settings.templates_dir))

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.get("/health")
def health():
    return {"status": "ok"}

from concurrent.futures import ThreadPoolExecutor

@app.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        print("[1/3] Generating story...")
        story = generate_story(story_prompt, character_name, setting, tone, art_style)
        print("[2/3] Generating 5 panels in parallel...")
        
        def process_panel(p):
            p["image_url"] = generate_image(
                p["image_prompt"], p["panel_number"],
                p["caption"], p["dialogue"], art_style
            )
            return p

        with ThreadPoolExecutor(max_workers=5) as executor:
            list(executor.map(process_panel, story["panels"]))

        print("[3/3] Building comic and PDF...")
        comic_url = build_comic(story)
        pdf_url = build_pdf(story)
        return templates.TemplateResponse(
            request=request, name="result.html",
            context={"story": story, "comic_url": comic_url, "pdf_url": pdf_url}
        )
    except Exception as exc:
        print(f"[ERROR] {exc!r}")
        return templates.TemplateResponse(
            request=request, name="error.html",
            context={"error": str(exc)}, status_code=500
        )
