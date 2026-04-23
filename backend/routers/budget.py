from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, or_
from typing import List, Optional
from datetime import datetime
import models, schemas
from database import get_db

router = APIRouter()

@router.get("/budget/current")
def get_budget(db: Session = Depends(get_db)):
    now = datetime.now()

    budget = db.query(models.MonthlyBudget).filter(
        models.MonthlyBudget.user_id == USER_ID_MOCK,
        models.MonthlyBudget.year == now.year,
        models.MonthlyBudget.month == now.month
    ).first()

    return {
        "amount": budget.amount if budget else 0
    }
    

@router.put("/budget/current")
def set_budget(payload: dict, db: Session = Depends(get_db)):
    now = datetime.now()

    budget = db.query(models.MonthlyBudget).filter(
        models.MonthlyBudget.user_id == USER_ID_MOCK,
        models.MonthlyBudget.year == now.year,
        models.MonthlyBudget.month == now.month
    ).first()

    if not budget:
        budget = models.MonthlyBudget(
            user_id=USER_ID_MOCK,
            year=now.year,
            month=now.month,
            amount=payload["amount"]
        )
        db.add(budget)
    else:
        budget.amount = payload["amount"]

    db.commit()
    db.refresh(budget)

    return budget