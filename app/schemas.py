from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel


# ---------- User Schemas ----------

class UserCreate(BaseModel):
    name: str
    age: int


class UserResponse(BaseModel):
    id: UUID
    name: str
    age: int

    class Config:
        from_attributes = True


# ---------- Income Schemas ----------

class IncomeCreate(BaseModel):
    user_id: UUID
    month: str
    income: Decimal


# ---------- Expense Schemas ----------

class ExpenseCreate(BaseModel):
    user_id: UUID
    month: str
    description: str
    amount: Decimal


class ExpenseResponse(BaseModel):
    description: str
    amount: Decimal
    ai_category: str
    percentage_of_income: float


# ---------- Analysis Schemas ----------

class AnalysisResponse(BaseModel):
    total_income: Decimal
    total_spent: Decimal
    needs_percentage: float
    wants_percentage: float
    invest_percentage: float
    tips: list[str]
