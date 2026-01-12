import os
import google.generativeai as genai
from typing import Optional  # <--- IMPORT THIS

# Load API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    USE_GEMINI = True
    print("✅ GEMINI_API_KEY loaded.")
else:
    USE_GEMINI = False
    print("⚠️ GEMINI_API_KEY missing. AI features disabled.")

# ---------------------------------------------------------
# FIX: Use "Optional[str]" instead of "str | None"
# ---------------------------------------------------------
def call_gemini(prompt: str) -> Optional[str]:  
    if not USE_GEMINI:
        return None

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        
        # Check if response is valid
        if response and response.text:
            return response.text.strip()
        
        return None

    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return None
