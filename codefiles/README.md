# ComicCraft - AI Fantasy Comic Creator

## Run in Antigravity / VS Code on Windows

1. Open this folder.
2. Open a terminal.
3. Create the virtual environment:
   `py -m venv .venv`
4. Install packages:
   `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
5. Copy `.env.example` to `.env`.
6. Put your Gemini API key in `.env`.
7. Start:
   `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`
8. Open http://127.0.0.1:8000

The app never waits forever for image generation. If Gemini image generation is rate-limited/unavailable, it creates a local artistic comic panel instead.
