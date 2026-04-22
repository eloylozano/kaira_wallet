from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
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

        # Limpiar campos que no pertenecen al modelo de BD
        data.pop("currency", None)

        # Procesar fecha
        if data.get("date") is None:
            data["date"] = datetime.now()
        elif isinstance(data["date"], str):
            data["date"] = datetime.fromisoformat(data["date"].replace("Z", "+00:00"))

        db_transaction = models.Transaction(
            type=data["type"],
            amount=data["amount"],
            date=data["date"],
            category_id=data["category_id"],
            is_paid=data.get("is_paid", True),
            frequency=data.get("frequency", "variable"),
            description=data.get("description") or "Nueva transacción",
            notes=data.get("notes") or data.get("description"),
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
    is_paid: Optional[bool] = None,
    sort: Optional[str] = "desc",
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Transaction).filter(
            models.Transaction.user_id == USER_ID_MOCK
        )

        if frequency:
            query = query.filter(models.Transaction.frequency == frequency)

        if transaction_type:
            query = query.filter(models.Transaction.type == transaction_type)

        if is_paid is not None:
            query = query.filter(models.Transaction.is_paid == is_paid)

        order = desc(models.Transaction.date) if sort == "desc" else asc(models.Transaction.date)

        results = (
            query
            .order_by(order)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return results

    except Exception as e:
        print(f"❌ ERROR al obtener transacciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/count")
def count_transactions(
    transaction_type: Optional[schemas.TransactionType] = None,
    is_paid: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Transaction).filter(models.Transaction.user_id == USER_ID_MOCK)

        if transaction_type:
            query = query.filter(models.Transaction.type == transaction_type)

        if is_paid is not None:
            query = query.filter(models.Transaction.is_paid == is_paid)

        return {"total": query.count()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # --- OBTENER UNA SOLA TRANSACCIÓN ---
@router.get("/{transaction_id}", response_model=schemas.TransactionWithCategory)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == USER_ID_MOCK
    ).first()
    
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    return db_transaction

@router.put("/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int, 
    transaction_update: schemas.TransactionCreate, # O un esquema Update si prefieres campos opcionales
    db: Session = Depends(get_db)
):
    db_query = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == USER_ID_MOCK
    )
    
    db_transaction = db_query.first()
    
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    update_data = transaction_update.model_dump()
    
    update_data.pop("currency", None)
    # Manejo de la fecha si viene como string
    if isinstance(update_data.get("date"), str):
        update_data["date"] = datetime.fromisoformat(update_data["date"].replace("Z", "+00:00"))

    db_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# --- ELIMINAR TRANSACCIÓN ---
@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == USER_ID_MOCK
    ).first()

    if not db_transaction:
        raise HTTPException(status_code=404, detail="No existe la transacción")

    db.delete(db_transaction)
    db.commit()
    return {"message": "Eliminada correctamente"}