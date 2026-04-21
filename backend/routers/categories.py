from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])
USER_ID_MOCK = 1 # Para que la BD siga funcionando sin login

@router.get("/predefined", response_model=List[schemas.CategoryWithSubcategories])
def get_predefined_categories(transaction_type: schemas.TransactionType = None, db: Session = Depends(get_db)):
    query = db.query(models.Category).filter(models.Category.is_predefined == True, models.Category.parent_id == None)
    if transaction_type:
        query = query.filter(models.Category.transaction_type == transaction_type)
    return query.all()

@router.post("/", response_model=schemas.Category)
def create_custom_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.model_dump(), user_id=USER_ID_MOCK, is_predefined=False)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=List[schemas.CategoryWithSubcategories])
def get_all_categories(transaction_type: schemas.TransactionType = None, db: Session = Depends(get_db)):
    query = db.query(models.Category).filter(
        models.Category.parent_id == None,
        ((models.Category.is_predefined == True) | (models.Category.user_id == USER_ID_MOCK))
    )
    if transaction_type:
        query = query.filter(models.Category.transaction_type == transaction_type)
    return query.all()