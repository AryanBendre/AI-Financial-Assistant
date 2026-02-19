import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, income, expense, analysis
from app.database import engine   # <--- Import the DB engine
from app import models            # <--- Import the models

# =======================================================
# 🏗️ THE FIX: BUILD THE TABLES AUTOMATICALLY
# This reads models.py and creates the empty tables in the DB
# =======================================================
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Based Personal Financial Awareness Assistant",
    description="An AI-powered financial awareness and advisory assistant.",
    version="1.0.0"
)

# --- 1. SETUP PATHS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static") # static is in the same folder as main.py
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# --- 2. MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. HEALTH CHECK ---
@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- 4. ROUTERS ---
app.include_router(user.router)
app.include_router(income.router)
app.include_router(expense.router)
app.include_router(analysis.router)

# --- 5. SERVE FRONTEND ---
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

