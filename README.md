# GrowthX Backend

FastAPI backend for GrowthX, a personal growth and habit-tracking app. Handles auth, habit/study/gym/water/weight tracking, dashboard aggregation, and an AI assistant with document-based Q&A (RAG).

**Live API:** https://growthx-backend-2ihu.onrender.com (interactive docs at `/docs`)
**Frontend repo:** https://github.com/Harshagnih0tri/GrowthX
**Live app:** https://spiffy-semifreddo-62fb07.netlify.app/

## Features

- JWT authentication (register/login)
- Habits CRUD, scoped per user
- Daily progress tracking (study minutes, gym status, water intake, weight)
- Goals CRUD
- Dashboard aggregation endpoint
- User profile
- AI assistant: Groq-powered chat, conversation history, document upload with embedding-based retrieval so the assistant can answer from a user's own uploaded documents
- Alembic-managed PostgreSQL schema

## Tech stack

FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL (`psycopg2`), `python-jose` + `passlib`/`bcrypt` for JWT auth, the Groq SDK for chat, Google GenAI for embeddings, `pypdf` for document parsing, served with Uvicorn.

## Architecture

```
app/
  main.py         # app assembly only — no business logic here
  config.py       # settings, loaded from environment variables
  database.py     # SQLAlchemy engine/session, get_db() dependency
  routers/        # HTTP layer — request in, response out
  models/         # SQLAlchemy ORM models
  schemas/        # Pydantic request/response contracts
  services/       # business logic
  repositories/   # database query layer
  core/           # JWT/security helpers, shared dependencies
```

Layered flow: a router validates the request and calls a service; the service holds business logic and calls a repository; the repository is the only layer that talks to the database.

## Local setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file (see **Environment variables** below).
4. Run migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Check it's alive: `http://127.0.0.1:8000/health`, and browse the API at `http://127.0.0.1:8000/docs`.

## Environment variables

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing secret — set a strong, unique value in production |
| `ALGORITHM` | JWT algorithm (defaults to `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT lifetime |
| `GROQ_API_KEY` | Groq API key, powers the AI assistant |
| `GROQ_MODEL` | Groq model name |
| `GEMINI_API_KEY` | Google GenAI key, used for document embeddings |

None of these have safe production defaults baked into the code — `.env` (or your host's environment settings) is required.

## Deployment

Deployed on Render, auto-redeploying on push to `main`. CORS is intentionally open (`allow_origins=["*"]`) since auth is a Bearer token in the `Authorization` header rather than cookies, so there's no credentialed-request risk in allowing any origin.
