from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud
from app.analysis_service import analyze_finances

router = APIRouter(prefix="/analysis", tags=["Analysis"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}/{month}")
def get_analysis(user_id: str, month: str, db: Session = Depends(get_db)):
    income_row = crud.get_income(db, user_id, month)
    if not income_row:
        raise HTTPException(status_code=404, detail="Income not found")

    expenses = crud.get_expenses(db, user_id, month)
    return analyze_finances(income_row.income, expenses)
