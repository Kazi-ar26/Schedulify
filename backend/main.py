"""
Schedulify Backend - FastAPI Application

Entry point for the centralized backend API.

Run with:
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

Requires:
    DATABASE_URL or SCHEDULIFY_DB_* environment variables
    SCHEDULIFY_SECRET_KEY (for JWT tokens)
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.routes import (
    auth,
    tasks,
    schedules,
    calendar,
    analytics,
    notifications,
    settings,
    users,
)


# -------------------------------------------------
# App Lifecycle
# -------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    logging.info("Starting Schedulify Backend...")
    init_db()
    logging.info("Schedulify Backend ready.")
    yield
    logging.info("Schedulify Backend shutting down.")


# -------------------------------------------------
# FastAPI App
# -------------------------------------------------

app = FastAPI(
    title="Schedulify API",
    description="Centralized backend for the Schedulify student productivity platform.",
    version="2.0.0",
    lifespan=lifespan,
)


# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Routes
# -------------------------------------------------

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(schedules.router)
app.include_router(calendar.router)
app.include_router(analytics.router)
app.include_router(notifications.router)
app.include_router(settings.router)


# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "schedulify-api", "version": "2.0.0"}
