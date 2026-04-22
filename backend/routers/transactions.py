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
        user = db.query(models.User).filter(models.User.id == USER_ID_MOCK).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuario {USER_ID_MOCK} no existe")

        category = db.query(models.Category).filter(models.Category.id == transaction.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail=f"Categoría {transaction.category_id} no existe")

        data = transaction.model_dump()

        # ❌ limpiar campos que no van al modelo
        data.pop("currency", None)

        # ⏱ fecha
        if data.get("date") is None:
            data["date"] = datetime.now()
        elif isinstance(data["date"], str):
            data["date"] = datetime.fromisoformat(data["date"].replace("Z", "+00:00"))

        # 💡 MAPEO CLARO (ESTO ES LA CLAVE)
        description = data.get("description")
        notes = data.get("notes")

        db_transaction = models.Transaction(
            type=data["type"],
            amount=data["amount"],
            date=data["date"],
            category_id=data["category_id"],
            is_paid=data.get("is_paid", True),
            frequency=data.get("frequency", "variable"),
            description=description,
            notes=notes,
            user_id=USER_ID_MOCK
        )

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
    is_paid: Optional[bool] = None,  # <-- Nuevo filtro para pagados/pendientes
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Transaction).filter(models.Transaction.user_id == USER_ID_MOCK)
        
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