# Vinay AI Studio

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
