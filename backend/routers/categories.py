from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas
from database import get_db
# Importamos la lógica de seguridad que ya tienes en main o dependencies
# Por ahora mantenemos el MOCK si quieres probar sin token, o usamos get_current_user
# from main import get_current_user 

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    redirect_slashes=True # Esto ayuda a manejar /categories y /categories/ automáticamente
)

@router.get("/", response_model=List[schemas.CategoryWithSubcategories])
def get_all_categories(
    transaction_type: Optional[schemas.TransactionType] = None, 
    db: Session = Depends(get_db)
):
    # Aquí puedes decidir si usar el ID 1 fijo o el usuario del token
    user_id = 1 
    
    query = db.query(models.Category).filter(
        models.Category.parent_id == None,
        ((models.Category.is_predefined == True) | (models.Category.user_id == user_id))
    )
    
    if transaction_type:
        query = query.filter(models.Category.transaction_type == transaction_type)
        
    return query.all()

@router.get("/predefined", response_model=List[schemas.CategoryWithSubcategories])
def get_predefined_categories(
    transaction_type: Optional[schemas.TransactionType] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Category).filter(
        models.Category.is_predefined == True, 
        models.Category.parent_id == None
    )
    
    if transaction_type:
        query = query.filter(models.Category.transaction_type == transaction_type)
        
    return query.all()

@router.post("/", response_model=schemas.Category)
def create_custom_category(
    category: schemas.CategoryCreate, 
    db: Session = Depends(get_db)
):
    user_id = 1
    db_category = models.Category(
        **category.model_dump(), 
        user_id=user_id, 
        is_predefined=False
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category