from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas
from database import get_db
from sqlalchemy.orm import joinedload
# Importamos la lógica de seguridad que ya tienes en main o dependencies
# Por ahora mantenemos el MOCK si quieres probar sin token, o usamos get_current_user
# from main import get_current_user 

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    redirect_slashes=True # Esto ayuda a manejar /categories y /categories/ automáticamente
)


@router.get("/", response_model=List[schemas.TransactionWithCategory])
def get_transactions(
    frequency: Optional[schemas.FrequencyType] = None,
    transaction_type: Optional[schemas.TransactionType] = None,
    is_paid: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Transaction).options(
            joinedload(models.Transaction.category)  # 🔥 ESTO ES CLAVE
        ).filter(models.Transaction.user_id == USER_ID_MOCK)

        if frequency:
            query = query.filter(models.Transaction.frequency == frequency)
        if transaction_type:
            query = query.filter(models.Transaction.type == transaction_type)
        if is_paid is not None:
            query = query.filter(models.Transaction.is_paid == is_paid)

        return query.order_by(models.Transaction.date.desc()).all()

    except Exception as e:
        print(f"❌ ERROR al obtener transacciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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