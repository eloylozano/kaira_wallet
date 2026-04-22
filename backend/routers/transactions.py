from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import models, schemas
from database import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])
USER_ID_MOCK = 1

@router.post("/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        # Validar que el usuario existe
        user = db.query(models.User).filter(models.User.id == USER_ID_MOCK).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuario {USER_ID_MOCK} no existe")
        
        # Validar que la categoría existe
        category = db.query(models.Category).filter(models.Category.id == transaction.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail=f"Categoría {transaction.category_id} no existe")
        
        # 1. Convertimos el esquema a diccionario
        transaction_data = transaction.model_dump()
        
        # 2. LIMPIEZA: Eliminamos 'currency' porque NO existe en models.Transaction
        # Usamos .pop con None para que no falle si el campo no viene
        transaction_data.pop('currency', None)
        
        # Si no se proporciona date, usar la fecha actual
        if transaction_data.get('date') is None:
            transaction_data['date'] = datetime.now()
        
        # 3. Ahora ya puedes desempaquetar con seguridad
        db_transaction = models.Transaction(**transaction_data, user_id=USER_ID_MOCK)
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ ERROR al crear transacción: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.TransactionWithCategory])
def get_transactions(
    frequency: Optional[schemas.FrequencyType] = None,
    transaction_type: Optional[schemas.TransactionType] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Transaction).filter(models.Transaction.user_id == USER_ID_MOCK)
        if frequency:
            query = query.filter(models.Transaction.frequency == frequency)
        if transaction_type:
            query = query.filter(models.Transaction.type == transaction_type)
        return query.order_by(models.Transaction.date.desc()).all()
    except Exception as e:
        print(f"❌ ERROR al obtener transacciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))