from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    base_dir = BASE_DIR
    static_dir = BASE_DIR / "static"
    panels_dir = static_dir / "panels"
    exports_dir = static_dir / "exports"
    templates_dir = BASE_DIR / "templates"

    gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
    text_model = os.getenv("GEMINI_TEXT_MODEL", "gemini-3.6-flash").strip()
    image_model = os.getenv("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image").strip()
    image_timeout = int(os.getenv("IMAGE_TIMEOUT_SECONDS", "45"))

    def ensure_dirs(self):
        self.static_dir.mkdir(exist_ok=True)
        self.panels_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_dirs()
