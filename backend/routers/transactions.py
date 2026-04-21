from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])
USER_ID_MOCK = 1

@router.post("/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.Transaction(**transaction.model_dump(), user_id=USER_ID_MOCK)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[schemas.TransactionWithCategory])
def get_transactions(frequency: schemas.FrequencyType = None, transaction_type: schemas.TransactionType = None, db: Session = Depends(get_db)):
    query = db.query(models.Transaction).filter(models.Transaction.user_id == USER_ID_MOCK)
    if frequency:
        query = query.filter(models.Transaction.frequency == frequency)
    if transaction_type:
        query = query.filter(models.Transaction.type == transaction_type)
    return query.order_by(models.Transaction.date.desc()).all()