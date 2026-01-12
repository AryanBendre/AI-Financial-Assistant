from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas
from app.ai_categorizer import categorize_expense

router = APIRouter(prefix="/expense", tags=["Expense"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= ADD EXPENSE =================
@router.post("/")
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    ai_category, ai_reason = categorize_expense(expense.description)

    db_expense = crud.add_expense(db, expense, ai_category)

    return {
        "id": db_expense.id,                 # ✅ REQUIRED
        "description": db_expense.description,
        "amount": db_expense.amount,
        "ai_category": db_expense.ai_category,
        "ai_reason": ai_reason
    }


# ================= DELETE EXPENSE =================
@router.delete("/{expense_id}")
def delete_expense(expense_id: str, db: Session = Depends(get_db)):
    expense = crud.delete_expense(db, expense_id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"message": "Expense deleted successfully"}


# ================= UPDATE EXPENSE =================
@router.put("/{expense_id}")
def update_expense(expense_id: str, payload: dict, db: Session = Depends(get_db)):
    description = payload.get("description")
    amount = payload.get("amount")

    if not description or amount is None:
        raise HTTPException(status_code=400, detail="Invalid input")

    ai_category, ai_reason = categorize_expense(description)

    expense = crud.update_expense(db, expense_id, description, amount)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.ai_category = ai_category
    db.commit()
    db.refresh(expense)

    return {
        "id": expense.id,
        "description": expense.description,
        "amount": expense.amount,
        "ai_category": ai_category,
        "ai_reason": ai_reason
    }
