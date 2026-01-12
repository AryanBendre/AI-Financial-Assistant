import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, income, expense, analysis

app = FastAPI(
    title="AI-Based Personal Financial Awareness Assistant",
    description="An AI-powered financial awareness and advisory assistant.",
    version="1.0.0"
)

# --- 1. SETUP PATHS ---
# This ensures we find the 'static' folder correctly, no matter where the server starts
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

# --- 2. MIDDLEWARE ---
# (Kept just in case, but less critical now that we are merged)
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

# --- 5. SERVE FRONTEND (Crucial Step) ---
# This tells FastAPI: "Serve index.html and other files from the static folder"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")