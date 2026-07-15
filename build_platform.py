import os
import zipfile

# ============================================================================
# Vinay AI Studio — single-file project generator
# ----------------------------------------------------------------------------
# What changed from the old version:
#   - Removed the "YouTube Channels" footer block entirely.
#   - Audio Enhance / Code Assistant / Translator Pro / Video Editor / Chat
#     Assistant are no longer separate broken columns — they are now ONE
#     unified chat console with a mode switcher. One input box, one output
#     stream, five modes.
#   - Wired to a genuinely FREE API (Groq's OpenAI-compatible endpoint,
#     free tier, no credit card needed) via an environment variable —
#     no key is hardcoded anywhere in this file or in git.
#   - New visual identity: deep indigo/plum background, soft periwinkle +
#     teal accents (nothing neon/loud), glass-panel chat console, short
#     text-based "Vinay AI" wordmark logo (no image asset to break).
#   - Footer contact icons: LinkedIn, Indeed, WhatsApp, X only — nothing
#     else was added, exactly as requested.
# ============================================================================

files_structure = {

    # ------------------------------------------------------------------
    # FRONTEND — single unified chat console (served by the backend too)
    # ------------------------------------------------------------------
    "frontend/public/manifest.json": """{
  "short_name": "VinayAI",
  "name": "Vinay AI Studio",
  "icons": [
    { "src": "icon-192.png", "type": "image/png", "sizes": "192x192" },
    { "src": "icon-512.png", "type": "image/png", "sizes": "512x512" }
  ],
  "start_url": "/?source=pwa",
  "background_color": "#120E26",
  "theme_color": "#120E26",
  "display": "standalone"
}""",

    "frontend/public/robots.txt": """User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Sitemap: https://vinayai.com/sitemap.xml""",

    "frontend/public/sitemap.xml": """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://vinayai.com/</loc>
    <lastmod>2026-07-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>""",

    "frontend/public/index.html": r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Vinay AI Studio</title>
<meta name="description" content="Vinay AI Studio - one console for chat, code, translation and notes." />
<link rel="manifest" href="/manifest.json" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg-1:#120E26;
    --bg-2:#1D1740;
    --surface:rgba(255,255,255,0.045);
    --surface-border:rgba(255,255,255,0.09);
    --text-hi:#EDEAF7;
    --text-lo:#A79FC7;
    --accent:#8C7BFA;
    --accent-2:#4FD1C5;
    --radius:18px;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;height:100%;}
  body{
    font-family:'Inter',system-ui,sans-serif;
    color:var(--text-hi);
    background:
      radial-gradient(1100px 600px at 12% -10%, rgba(140,123,250,0.16), transparent 60%),
      radial-gradient(900px 500px at 100% 0%, rgba(79,209,197,0.10), transparent 55%),
      linear-gradient(180deg,var(--bg-1),var(--bg-2) 55%, #150F2C 100%);
    min-height:100vh;
    display:flex;
    flex-direction:column;
  }
  .noise{
    position:fixed;inset:0;pointer-events:none;opacity:0.035;mix-blend-mode:overlay;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  }
  header{
    display:flex;align-items:center;justify-content:space-between;
    padding:22px clamp(20px,5vw,64px);
  }
  .logo{display:flex;align-items:center;gap:9px;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:19px;letter-spacing:-0.01em;}
  .logo .mark{
    width:26px;height:26px;border-radius:8px;flex:none;
    background:linear-gradient(135deg,var(--accent),var(--accent-2));
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 0 18px rgba(140,123,250,0.55);
  }
  .logo .mark svg{width:14px;height:14px;}
  .logo span.grad{background:linear-gradient(90deg,#fff,var(--accent) 90%);-webkit-background-clip:text;background-clip:text;color:transparent;}
  .logo .sub{font-family:'Inter';font-weight:500;font-size:11px;color:var(--text-lo);letter-spacing:0.14em;text-transform:uppercase;margin-left:2px;}
  main{
    flex:1;display:flex;flex-direction:column;align-items:center;
    padding:10px 20px 40px;
  }
  .intro{text-align:center;max-width:640px;margin:18px 0 28px;}
  .intro h1{
    font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:clamp(26px,4vw,38px);
    margin:0 0 10px;line-height:1.15;
  }
  .intro p{color:var(--text-lo);margin:0;font-size:15px;line-height:1.6;}
  .console{
    width:100%;max-width:760px;
    background:var(--surface);
    border:1px solid var(--surface-border);
    border-radius:var(--radius);
    backdrop-filter:blur(18px);
    -webkit-backdrop-filter:blur(18px);
    box-shadow:0 30px 80px -30px rgba(0,0,0,0.55);
    overflow:hidden;
    position:relative;
  }
  .console::before{
    content:"";position:absolute;inset:-1px;border-radius:var(--radius);padding:1px;
    background:linear-gradient(120deg, rgba(140,123,250,0.55), rgba(79,209,197,0.0) 30%, rgba(79,209,197,0.35) 70%, rgba(140,123,250,0.5));
    -webkit-mask:linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite:xor;mask-composite:exclude;
    pointer-events:none;opacity:0.6;animation:sheen 7s ease-in-out infinite;
  }
  @keyframes sheen{0%,100%{opacity:0.35;}50%{opacity:0.75;}}
  .modes{
    display:flex;gap:6px;padding:14px 16px;flex-wrap:wrap;
    border-bottom:1px solid var(--surface-border);
  }
  .mode-btn{
    font-family:'Inter';font-size:13px;font-weight:500;color:var(--text-lo);
    background:transparent;border:1px solid transparent;border-radius:999px;
    padding:7px 14px;cursor:pointer;transition:all .15s ease;
  }
  .mode-btn:hover{color:var(--text-hi);}
  .mode-btn.active{
    color:#12102A;background:linear-gradient(90deg,var(--accent),var(--accent-2));
    font-weight:600;
  }
  #log{
    height:420px;overflow-y:auto;padding:22px;display:flex;flex-direction:column;gap:14px;
  }
  .msg{max-width:82%;padding:11px 15px;border-radius:14px;font-size:14.5px;line-height:1.55;white-space:pre-wrap;}
  .msg.user{align-self:flex-end;background:linear-gradient(135deg,var(--accent),#6E5CE0);color:#fff;border-bottom-right-radius:4px;}
  .msg.bot{align-self:flex-start;background:rgba(255,255,255,0.06);border:1px solid var(--surface-border);color:var(--text-hi);border-bottom-left-radius:4px;}
  .msg.err{align-self:flex-start;background:rgba(255,90,90,0.08);border:1px solid rgba(255,90,90,0.3);color:#ffb3b3;}
  .msg.system{align-self:center;color:var(--text-lo);font-size:13px;background:none;}
  .composer{display:flex;gap:10px;padding:16px;border-top:1px solid var(--surface-border);}
  #input{
    flex:1;resize:none;min-height:46px;max-height:140px;
    background:rgba(255,255,255,0.05);border:1px solid var(--surface-border);
    border-radius:12px;color:var(--text-hi);padding:12px 14px;font-family:'Inter';font-size:14.5px;
    outline:none;
  }
  #input:focus{border-color:var(--accent);}
  #send{
    flex:none;border:none;border-radius:12px;padding:0 20px;font-weight:600;font-size:14px;
    color:#12102A;background:linear-gradient(90deg,var(--accent),var(--accent-2));cursor:pointer;
  }
  #send:disabled{opacity:0.5;cursor:not-allowed;}
  footer{padding:26px 20px 34px;text-align:center;}
  .contact{display:flex;justify-content:center;gap:16px;margin-bottom:14px;}
  .contact a{
    width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;
    background:var(--surface);border:1px solid var(--surface-border);color:var(--text-lo);
    transition:all .15s ease;
  }
  .contact a:hover{color:var(--text-hi);border-color:var(--accent);transform:translateY(-2px);}
  .contact svg{width:17px;height:17px;fill:currentColor;}
  footer p{color:var(--text-lo);font-size:12.5px;margin:0;}
  @media(max-width:480px){ #log{height:360px;} }
</style>
</head>
<body>
<div class="noise"></div>

<header>
  <div class="logo">
    <span class="mark"><svg viewBox="0 0 24 24" fill="none"><path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z" fill="white"/></svg></span>
    <span class="grad">Vinay AI</span>
    <span class="sub">Studio</span>
  </div>
</header>

<main>
  <div class="intro">
    <h1>One console. Every task.</h1>
    <p>Chat, write code, translate, and turn audio or video notes into something useful — all in a single conversation.</p>
  </div>

  <div class="console">
    <div class="modes" id="modes">
      <button class="mode-btn active" data-mode="chat">Chat</button>
      <button class="mode-btn" data-mode="code">Code Assistant</button>
      <button class="mode-btn" data-mode="translate">Translator Pro</button>
      <button class="mode-btn" data-mode="audio">Audio Notes</button>
      <button class="mode-btn" data-mode="video">Video Notes</button>
    </div>

    <div id="log">
      <div class="msg system">Pick a mode above, then start typing. Everything happens right here in one chat.</div>
    </div>

    <div class="composer">
      <textarea id="input" placeholder="Message Vinay AI..." rows="1"></textarea>
      <button id="send">Send</button>
    </div>
  </div>

  <footer>
    <div class="contact">
      <a href="#" title="LinkedIn" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.03-1.85-3.03-1.85 0-2.14 1.45-2.14 2.94v5.66H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.13 2.07 2.07 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45z"/></svg>
      </a>
      <a href="#" title="Indeed" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24"><path d="M12.02 2.02c-.94 0-1.7.76-1.7 1.7v.3a1.7 1.7 0 0 0 3.4 0v-.3c0-.94-.76-1.7-1.7-1.7zM10.4 8.9h3.2v12.6a2.5 2.5 0 0 1-2.5 2.5h-.2a2.5 2.5 0 0 1-2.5-2.5V11.4a2.5 2.5 0 0 1 2-2.5z"/></svg>
      </a>
      <a href="#" title="WhatsApp" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.15-1.7-.85-2-.95-.27-.1-.46-.15-.66.15-.2.3-.75.94-.92 1.13-.17.2-.34.22-.63.08-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.65-2.05-.17-.3-.02-.46.13-.6.13-.14.3-.34.44-.51.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.66-1.6-.9-2.18-.24-.58-.48-.5-.66-.5h-.56c-.2 0-.52.08-.79.37-.27.3-1.03 1.01-1.03 2.46s1.06 2.86 1.2 3.06c.15.2 2.1 3.2 5.08 4.5.71.3 1.26.49 1.7.62.71.23 1.36.2 1.87.12.57-.08 1.7-.7 1.94-1.36.24-.67.24-1.24.17-1.36-.07-.12-.26-.2-.55-.35zM12.02 2C6.5 2 2 6.48 2 12c0 1.8.48 3.55 1.38 5.08L2 22l5.05-1.33A9.96 9.96 0 0 0 12.02 22C17.55 22 22 17.52 22 12S17.55 2 12.02 2z"/></svg>
      </a>
      <a href="#" title="X" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24"><path d="M18.24 3H21l-6.55 7.49L22 21h-6.3l-4.93-6.44L4.9 21H2.13l7-8L2 3h6.44l4.46 5.9L18.24 3zm-1.1 16.17h1.74L7.02 4.74H5.15l12 14.43z"/></svg>
      </a>
    </div>
    <p>&copy; 2026 Vinay AI Studio. Built for creators and builders.</p>
  </footer>
</main>

<script>
const log = document.getElementById('log');
const input = document.getElementById('input');
const sendBtn = document.getElementById('send');
const modeBtns = document.querySelectorAll('.mode-btn');
let mode = 'chat';
let history = [];

modeBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    modeBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    mode = btn.dataset.mode;
  });
});

input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = Math.min(input.scrollHeight, 140) + 'px';
});
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
});
sendBtn.addEventListener('click', send);

function addMsg(text, cls){
  const d = document.createElement('div');
  d.className = 'msg ' + cls;
  d.textContent = text;
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
  return d;
}

async function send(){
  const text = input.value.trim();
  if(!text) return;
  addMsg(text, 'user');
  history.push({role:'user', content:text});
  input.value = ''; input.style.height='auto';
  sendBtn.disabled = true;
  const thinking = addMsg('Thinking...', 'bot');

  try{
    const res = await fetch('/api/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ message:text, mode:mode, history:history.slice(-10) })
    });
    const data = await res.json();
    if(!res.ok){ throw new Error(data.detail || 'Something went wrong.'); }
    thinking.textContent = data.reply;
    history.push({role:'assistant', content:data.reply});
  }catch(err){
    thinking.textContent = err.message;
    thinking.className = 'msg err';
  }finally{
    sendBtn.disabled = false;
  }
}
</script>
</body>
</html>""",

    # ------------------------------------------------------------------
    # BACKEND — one FastAPI app, one /api/chat endpoint, five modes
    # ------------------------------------------------------------------
    "backend/app/main.py": '''import os
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
''',

    "backend/requirements.txt": """fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.9.2
httpx==0.27.2""",

    "backend/app/multi_tenant_platform.py": """import uuid
import time
from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class OrgTenant:
    id: str
    name: str
    custom_domain: str
    billing_status: str = "Active"
    branding: Dict[str, str] = field(default_factory=lambda: {"primary_color": "#8C7BFA", "secondary_color": "#4FD1C5"})

@dataclass
class TeamMember:
    id: str
    org_id: str
    email: str
    role: str
    department: str

class EnterpriseCollaborationPlatform:
    def __init__(self):
        self.tenants = {}
        self.members = {}
        self.rate_limits = {}

    def create_tenant(self, name: str, domain: str) -> OrgTenant:
        tenant_id = f"org_{uuid.uuid4().hex[:8]}"
        tenant = OrgTenant(id=tenant_id, name=name, custom_domain=domain)
        self.tenants[tenant_id] = tenant
        self.members[tenant_id] = []
        return tenant

    def add_member(self, org_id: str, email: str, role: str, department: str) -> TeamMember:
        if org_id not in self.tenants:
            raise KeyError("Invalid Org ID")
        member = TeamMember(id=f"usr_{uuid.uuid4().hex[:8]}", org_id=org_id, email=email, role=role, department=department)
        self.members[org_id].append(member)
        return member

    def verify_isolation_gate(self, actor: TeamMember, target_org_id: str) -> bool:
        if actor.org_id != target_org_id:
            raise PermissionError(f"SECURITY ALERT: Unauthorized access attempt by {actor.id}")
        return True

    def configure_api_key(self, org_id: str, key_alias: str, rps_limit: int = 10):
        self.rate_limits[org_id] = {"alias": key_alias, "max_rps": rps_limit, "current_hits": 0, "window_start": time.time()}

    def check_rate_limit(self, org_id: str) -> bool:
        policy = self.rate_limits.get(org_id)
        if not policy:
            return True
        now = time.time()
        if now - policy["window_start"] > 1.0:
            policy["current_hits"] = 1
            policy["window_start"] = now
            return True
        if policy["current_hits"] >= policy["max_rps"]:
            return False
        policy["current_hits"] += 1
        return True
""",

    # ------------------------------------------------------------------
    # ENV / SECURITY — key never hardcoded, only referenced
    # ------------------------------------------------------------------
    "backend/.env.example": """# Copy this file to ".env" and fill in your own key. Never commit the real .env file.
# Get a FREE key (no credit card) at https://console.groq.com -> API Keys
GROQ_API_KEY=your_free_groq_key_here
GROQ_MODEL=llama-3.3-70b-versatile
PORT=8000""",

    ".gitignore": """.env
__pycache__/
*.pyc
.DS_Store
node_modules/
vinay_ai_enterprise.zip""",

    # ------------------------------------------------------------------
    # CI/CD
    # ------------------------------------------------------------------
    ".github/workflows/production-pipeline.yml": """name: Production Pipeline
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  build-and-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: pip install -r backend/requirements.txt
    - name: Import check
      run: python -c "import sys; sys.path.insert(0,'backend/app'); import main; print('OK')"
""",

    # ------------------------------------------------------------------
    # LEGAL
    # ------------------------------------------------------------------
    "legal/privacy_policy.md": """# Privacy Policy
Last updated: July 15, 2026

We do not sell your data. Chat messages are sent to our AI provider only to generate a response and are not stored beyond your session.""",

    "legal/terms_of_service.md": """# Terms of Service
Last updated: July 15, 2026

These terms govern the usage of Vinay AI Studio.""",

    "README.md": """# Vinay AI Studio

One unified AI console: Chat, Code Assistant, Translator Pro, Audio Notes, and Video Notes,
all inside a single chat interface.

## Local setup

1. `cd backend`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your free Groq key from https://console.groq.com
4. `python app/main.py`
5. Open http://localhost:8000

## Deploying

- **Render**: Build command `pip install -r backend/requirements.txt`, start command
  `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`. Add `GROQ_API_KEY` under
  Environment Variables in the Render dashboard.
- **Vercel**: better suited for the `frontend/` folder alone if you split frontend/backend;
  for this combined single-app setup, Render (or Railway/Fly.io) is recommended since the
  app runs as a persistent server.

## Getting a free API key

1. Go to https://console.groq.com
2. Sign up (no credit card required)
3. Create an API key
4. Set it as `GROQ_API_KEY` in your `.env` locally and in your host's environment variables
   — never paste it directly into any file that gets committed to git.
"""
}

# ----------------------------------------------------------------------
# Generate the files locally
# ----------------------------------------------------------------------
print("Creating files and folders structure locally...")
for path, content in files_structure.items():
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Created: {path}")

# ----------------------------------------------------------------------
# Zip everything up
# ----------------------------------------------------------------------
zip_filename = "vinay_ai_studio.zip"
print(f"Creating ZIP archive: {zip_filename}...")
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    for path in files_structure.keys():
        zipf.write(path)

print("\n" + "=" * 50)
print(f" SUCCESS: '{zip_filename}' created.")
print(" Remember: add your free GROQ_API_KEY as an environment")
print(" variable — do not put it inside any file you commit.")
print("=" * 50)
