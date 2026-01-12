from decimal import Decimal
from typing import List

from app.models import MonthlyExpense
from app.ai_tips import generate_ai_tips


def analyze_finances(
    income: Decimal,
    expenses: List[MonthlyExpense]
):
    total_spent = sum(exp.amount for exp in expenses)

    needs = sum(exp.amount for exp in expenses if exp.ai_category == "Needs")
    wants = sum(exp.amount for exp in expenses if exp.ai_category == "Wants")
    invest = sum(exp.amount for exp in expenses if exp.ai_category == "Invest")

    needs_pct = float((needs / income) * 100) if income else 0
    wants_pct = float((wants / income) * 100) if income else 0
    invest_pct = float((invest / income) * 100) if income else 0

    # 🔹 Gemini-based personalized tips (with fallback inside)
    tips = generate_ai_tips({
        "income": float(income),
        "needs_percentage": round(needs_pct, 2),
        "wants_percentage": round(wants_pct, 2),
        "invest_percentage": round(invest_pct, 2)
    })

    return {
        "total_income": income,
        "total_spent": total_spent,
        "needs_percentage": round(needs_pct, 2),
        "wants_percentage": round(wants_pct, 2),
        "invest_percentage": round(invest_pct, 2),
        "tips": tips
    }
