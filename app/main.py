import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, income, expense, analysis
from app.database import engine
from app import models

# =======================================================
# 🏗️ THE FIX: BUILD THE TABLES AUTOMATICALLY
# =======================================================
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Based Personal Financial Awareness Assistant",
    description="An AI-powered financial awareness and advisory assistant.",
    version="1.0.0"
)

# --- 1. SETUP PATHS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

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

# --- 4. ROUTERS (Register these BEFORE mounting static files) ---
# This ensures API requests like POST /user/ are handled by the routers.
app.include_router(user.router)
app.include_router(income.router)
app.include_router(expense.router)
app.include_router(analysis.router)

# --- 5. SERVE FRONTEND (The 'Catch-All' must be LAST) ---
# By placing this last, it only catches requests that don't match your API.
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
