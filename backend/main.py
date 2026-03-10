from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from database import get_db, engine, Base
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
import models
import schemas
from routers import chat, data, auth
from dependencies import get_current_user, get_admin_user

app = FastAPI(title="Campus Data Backend")

app.include_router(auth.router)
app.include_router(chat.router, dependencies=[Depends(get_current_user)])
app.include_router(data.router, dependencies=[Depends(get_admin_user)])

# Configure CORS
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
