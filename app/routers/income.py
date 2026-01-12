from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/income", tags=["Income"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    return crud.add_income(db, income)
