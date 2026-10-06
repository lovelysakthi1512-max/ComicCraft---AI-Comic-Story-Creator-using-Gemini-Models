import json
from google import genai
from .config import settings

FALLBACK_TEXT_MODELS = [
    settings.text_model,
    "gemini-3.8-flash",
    "gemini-3.1-pro-preview",
    "gemini-2.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-flash-latest",
]

def _client():
    if not settings.gemini_api_key:
        return None
    return genai.Client(api_key=settings.gemini_api_key)

def _local_fallback_story(prompt, character, setting, tone, art_style):
    char = character if character else "The Hero"
    loc = setting if setting else "The Mystic Realm"
    t = tone if tone else "Epic"
    
    return {
        "title": f"The Quest of {char}",
        "subtitle": f"An {t.lower()} adventure set in {loc}",
        "panels": [
            {
                "panel_number": 1,
                "caption": f"In the heart of {loc}, {char} discovers an unexpected secret.",
                "dialogue": f"{char}: 'Something ancient wakes in this realm...'",
                "image_prompt": f"{art_style} style, {char} standing dramatically in {loc}, discovering a glowing magical symbol, detailed fantasy artwork."
            },
            {
                "panel_number": 2,
                "caption": f"As {prompt.lower() or 'a mysterious energy rises'}, a shadow falls across the path.",
                "dialogue": f"{char}: 'I must prepare for whatever lies ahead.'",
                "image_prompt": f"{art_style} style, {char} looking up as dark energy swirls in {loc}, heroic pose, cinematic lighting."
            },
            {
                "panel_number": 3,
                "caption": "The challenge manifests in full force before the hero.",
                "dialogue": f"{char}: 'I will not back down!'",
                "image_prompt": f"{art_style} style, {char} engaging with a mythical guardian creature in {loc}, action shot, dynamic composition."
            },
            {
                "panel_number": 4,
                "caption": "Summoning inner strength, the decisive moment arrives.",
                "dialogue": f"{char}: 'By light and honor, let the power unleash!'",
                "image_prompt": f"{art_style} style, {char} channeling brilliant magical energy to overcome the obstacle in {loc}, epic climax."
            },
            {
                "panel_number": 5,
                "caption": "Victory achieved, peace settles over the lands once more.",
                "dialogue": f"{char}: 'The story has only just begun.'",
                "image_prompt": f"{art_style} style, {char} standing victorious on a high cliff overlooking {loc} at sunset, triumphant conclusion."
            }
        ]
    }

def generate_story(prompt, character, setting, tone, art_style):
    client = _client()
    if client:
        request = f'''
Create a 5-panel fantasy comic story for a student project.

User story idea: {prompt}
Main character: {character}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY valid JSON with this structure:
{{
  "title": "short title",
  "subtitle": "one sentence",
  "panels": [
    {{
      "panel_number": 1,
      "caption": "short caption",
      "dialogue": "short dialogue or narration",
      "image_prompt": "detailed visual prompt"
    }}
  ]
}}

Rules:
- Exactly 5 panels.
- Family-friendly and TN college-project appropriate.
- Clear beginning, middle, climax and ending.
- Keep dialogue short.
- Every image_prompt must describe the same main character consistently.
'''
        for model in dict.fromkeys(FALLBACK_TEXT_MODELS):
            try:
                print(f"[INFO] Story model: {model}")
                response = client.models.generate_content(
                    model=model,
                    contents=request,
                    config={"response_mime_type": "application/json"},
                )
                data = json.loads(response.text)
                if len(data.get("panels", [])) == 5:
                    return data
            except Exception as exc:
                print(f"[WARN] Text model failed: {model}: {exc}")
    
    print("[INFO] Using local fallback story generator (API rate limit / 503 protection).")
    return _local_fallback_story(prompt, character, setting, tone, art_style)

