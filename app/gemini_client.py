import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if USE_GEMINI and GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

print("USE_GEMINI:", USE_GEMINI)
print("GEMINI_API_KEY loaded:", bool(GEMINI_API_KEY))


def call_gemini(prompt: str) -> str | None:
    if not client:
        return None

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        print("Gemini error:", e)
        return None
