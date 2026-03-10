from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager

from database import engine, Base
import models
import schemas
from routers import chat, data, auth
from dependencies import get_current_user, get_admin_user
from seed import run_migrations, run_seed

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run Alembic migrations and seed data on startup
    run_migrations()
    run_seed()
    yield

app = FastAPI(title="Campus Data Backend", lifespan=lifespan)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(chat.router, dependencies=[Depends(get_current_user)])
app.include_router(data.router, dependencies=[Depends(get_admin_user)])

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.environ.get("DATABASE_URL")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.get("/api/test")
def test_connection():
    return {
        "status": "success",
        "message": "Hello from FastAPI Backend!",
        "database_url_configured": bool(DATABASE_URL),
        "gemini_api_key_configured": bool(GEMINI_API_KEY),
    }
