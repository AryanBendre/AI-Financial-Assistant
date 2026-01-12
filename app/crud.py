from sqlalchemy.orm import Session
from uuid import UUID

from app import models, schemas


# ---------- User ----------

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        age=user.age
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------- Income ----------

def add_income(db: Session, income: schemas.IncomeCreate):
    db_income = models.MonthlyIncome(
        user_id=income.user_id,
        month=income.month,
        income=income.income
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


def get_income(db: Session, user_id: UUID, month: str):
    return (
        db.query(models.MonthlyIncome)
        .filter(
            models.MonthlyIncome.user_id == user_id,
            models.MonthlyIncome.month == month
        )
        .first()
    )


# ---------- Expense ----------

def add_expense(db: Session, expense: schemas.ExpenseCreate, ai_category: str):
    db_expense = models.MonthlyExpense(
        user_id=expense.user_id,
        month=expense.month,
        description=expense.description,
        amount=expense.amount,
        ai_category=ai_category
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, user_id: UUID, month: str):
    return (
        db.query(models.MonthlyExpense)
        .filter(
            models.MonthlyExpense.user_id == user_id,
            models.MonthlyExpense.month == month
        )
        .all()
    )


# ---------- Expense Update / Delete ----------

def delete_expense(db: Session, expense_id):
    expense = db.query(models.MonthlyExpense).filter(
        models.MonthlyExpense.id == expense_id
    ).first()

    if expense:
        db.delete(expense)
        db.commit()

    return expense


def update_expense(db: Session, expense_id, description, amount):
    expense = db.query(models.MonthlyExpense).filter(
        models.MonthlyExpense.id == expense_id
    ).first()

    if not expense:
        return None

    expense.description = description
    expense.amount = amount

    return expense
