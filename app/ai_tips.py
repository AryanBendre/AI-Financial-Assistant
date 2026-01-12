from app.gemini_client import call_gemini

def generate_ai_tips(summary: dict) -> list[str]:
    prompt = f"""
You are a financial awareness assistant for an Indian salaried person.

Monthly income: ₹{summary['income']}
Needs spending: {summary['needs_percentage']}%
Wants spending: {summary['wants_percentage']}%
Invest spending: {summary['invest_percentage']}%

Give 3 short, practical, non-judgmental tips.
Avoid repeating generic advice.
"""

    response = call_gemini(prompt)
    print("Gemini response:", response)

    if not response:
        return [
            "Track expenses consistently to stay financially aware.",
            "Try balancing discretionary spending with savings.",
            "Small regular investments can build long-term discipline."
        ]

    return [tip.strip("- ").strip() for tip in response.split("\n") if tip.strip()]
    
