from typing import Tuple, Optional # <--- Added Optional
from app.gemini_client import call_gemini

NEEDS_KEYWORDS = [
    "rent", "electricity", "water", "bill", "grocery",
    "insurance", "emi", "loan", "school", "medical"
]

WANTS_KEYWORDS = [
    "zomato", "swiggy", "movie", "shopping",
    "trip", "netflix", "dining", "party"
]

INVEST_KEYWORDS = [
    "sip", "mutual fund", "ppf", "rd",
    "fd", "investment", "stocks"
]

# FIX: Changed "str | None" to "Optional[str]"
def rule_based_category(description: str) -> Tuple[Optional[str], Optional[str]]:
    desc = description.lower()

    for word in INVEST_KEYWORDS:
        if word in desc:
            return "Invest", "Identified as investment-related expense."

    for word in NEEDS_KEYWORDS:
        if word in desc:
            return "Needs", "Identified as essential living expense."

    for word in WANTS_KEYWORDS:
        if word in desc:
            return "Wants", "Identified as discretionary lifestyle expense."

    return None, None


def gemini_category(description: str) -> Tuple[str, str]:
    prompt = f
    """
You are a financial categorization assistant.

Classify the expense below into one category only:
Needs, Wants, or Invest.

Expense: "{description}"

Return response in this exact format:
Category: <Needs/Wants/Invest>
Reason: <short explanation>
"""
    response = call_gemini(prompt)

    if not response:
        return "Wants", "Defaulted due to unclear classification."

    try:
        lines = response.splitlines()
        category = lines[0].split(":")[1].strip()
        reason = lines[1].split(":")[1].strip()
        return category, reason
    except Exception:
        return "Wants", "Defaulted due to parsing error."


def categorize_expense(description: str) -> Tuple[str, str]:
    category, reason = rule_based_category(description)

    if category:
        return category, reason

    # Fallback to Gemini
    category, reason = gemini_category(description)
    return category, reason
