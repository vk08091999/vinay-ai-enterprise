import os
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Vinay AI Studio - unified backend
# One single /api/chat endpoint powers every mode (Chat, Code, Translate,
# Audio Notes, Video Notes). The frontend never talks to separate services -
# it just sends a "mode" flag and this file picks the right system prompt.
#
# Uses Groq's free-tier API (OpenAI-compatible). No key is hardcoded here -
# set GROQ_API_KEY as an environment variable on your machine and again in
# your hosting provider's dashboard (Render / Vercel / etc).
# ---------------------------------------------------------------------------

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

app = FastAPI(title="Vinay AI Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODE_PROMPTS = {
    "chat": "You are Vinay AI, a friendly and precise general-purpose assistant.",
    "code": "You are Vinay AI's Code Assistant. Answer with clean, correct, well-commented code. Explain briefly after the code block.",
    "translate": "You are Vinay AI's Translator Pro. Detect the source language and translate the user's text accurately. If the target language isn't stated, translate to English. Return only the translation plus the detected language on the first line.",
    "audio": "You are Vinay AI's Audio Notes assistant. The user will paste a transcript or describe an audio clip. Clean it up, fix grammar, and summarize key points clearly.",
    "video": "You are Vinay AI's Video Notes assistant. The user will describe or paste a video transcript/script. Produce a clean script outline, suggested cut points, and a short summary.",
}
VALID_MODES = set(MODE_PROMPTS.keys())


class ChatRequest(BaseModel):
    message: str
    mode: str = "chat"
    history: Optional[list] = None


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Vinay AI Studio", "key_configured": bool(GROQ_API_KEY)}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    mode = req.mode if req.mode in VALID_MODES else "chat"

    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Server is missing GROQ_API_KEY. Add it in your hosting provider's Environment Variables settings.",
        )

    messages = [{"role": "system", "content": MODE_PROMPTS[mode]}]
    if req.history:
        messages.extend(req.history[-10:])
    messages.append({"role": "user", "content": req.message})

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
    }
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(GROQ_API_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Upstream AI provider error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Could not reach AI provider: {str(e)}")

    reply = data["choices"][0]["message"]["content"]
    return {"mode": mode, "reply": reply}


# Serve the frontend from the same app, so one deploy covers the whole site.
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "public")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
