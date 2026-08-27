from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc, or_
from typing import List, Optional
from datetime import datetime

import models
import schemas
from database import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])
USER_ID_MOCK = 1


@router.post("/", response_model=schemas.TransactionWithCategory)
def create_transaction(
    transaction: schemas.TransactionCreate, 
    request: Request, 
    db: Session = Depends(get_db)
):
    try:
        account = request.state.account

        category = db.query(models.Category).filter(models.Category.id == transaction.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail=f"Categoría {transaction.category_id} no existe")

        data = transaction.model_dump()
        data.pop("currency", None)

        if data.get("date") is None:
            data["date"] = datetime.now()
        elif isinstance(data["date"], str):
            data["date"] = datetime.fromisoformat(data["date"].replace("Z", "+00:00"))

        db_transaction = models.Transaction(
            type=data["type"],
            amount=data["amount"],
            date=data["date"],
            category_id=data["category_id"],
            account_id=account.id,
            user_id=USER_ID_MOCK,
            is_paid=data.get("is_paid", True),
            frequency=data.get("frequency", "variable"),
            description=data.get("description") or "Nueva transacción",
            notes=data.get("notes") or data.get("description")
        )

        db.add(db_transaction)
        db.commit()

        # Recargamos incluyendo la relación category para el schema TransactionWithCategory
        return db.query(models.Transaction).options(
            joinedload(models.Transaction.category)
        ).filter(models.Transaction.id == db_transaction.id).first()

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.TransactionWithCategory])
def get_transactions(
    request: Request,
    frequency: Optional[schemas.FrequencyType] = None,
    transaction_type: Optional[schemas.TransactionType] = None,
    is_paid: Optional[bool] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "desc",
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        account = request.state.account

        query = db.query(models.Transaction).options(
            joinedload(models.Transaction.category)
        ).filter(
            models.Transaction.account_id == account.id
        )

        if frequency:
            query = query.filter(models.Transaction.frequency == frequency)

        if transaction_type:
            query = query.filter(models.Transaction.type == transaction_type)

        if is_paid is not None:
            query = query.filter(models.Transaction.is_paid == is_paid)

        if search:
            query = query.outerjoin(models.Category).filter(
                or_(
                    models.Transaction.description.ilike(f"%{search}%"),
                    models.Transaction.notes.ilike(f"%{search}%"),
                    models.Category.name.ilike(f"%{search}%")
                )
            )

        order = desc(models.Transaction.date) if sort == "desc" else asc(models.Transaction.date)
        return query.order_by(order).offset(skip).limit(limit).all()

    except Exception as e:
        print(f"❌ ERROR get_transactions: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener transacciones: {str(e)}")


@router.get("/count")
def count_transactions(
    request: Request,
    transaction_type: Optional[schemas.TransactionType] = None,
    is_paid: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    account = request.state.account
    query = db.query(models.Transaction).filter(models.Transaction.account_id == account.id)

    if transaction_type:
        query = query.filter(models.Transaction.type == transaction_type)

    if is_paid is not None:
        query = query.filter(models.Transaction.is_paid == is_paid)

    if search:
        query = query.outerjoin(models.Category).filter(
            or_(
                models.Transaction.description.ilike(f"%{search}%"),
                models.Transaction.notes.ilike(f"%{search}%"),
                models.Category.name.ilike(f"%{search}%")
            )
        )

    return {"total": query.count()}


@router.get("/{transaction_id}", response_model=schemas.TransactionWithCategory)
def get_transaction(
    transaction_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    account = request.state.account
    tx = db.query(models.Transaction).options(
        joinedload(models.Transaction.category)
    ).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.account_id == account.id
    ).first()

    if not tx:
        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )

    return tx


@router.put("/{transaction_id}", response_model=schemas.TransactionWithCategory)
def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        account = request.state.account

        db_transaction = db.query(models.Transaction).filter(
            models.Transaction.id == transaction_id,
            models.Transaction.account_id == account.id
        ).first()

        if not db_transaction:
            raise HTTPException(
                status_code=404,
                detail="Transacción no encontrada"
            )

        update_data = transaction_update.model_dump(exclude_unset=True)
        update_data.pop("currency", None)

        if isinstance(update_data.get("date"), str):
            update_data["date"] = datetime.fromisoformat(
                update_data["date"].replace("Z", "+00:00")
            )

        if "category_id" in update_data:
            category = db.query(models.Category).filter(
                models.Category.id == update_data["category_id"]
            ).first()

            if not category:
                raise HTTPException(
                    status_code=404,
                    detail="Categoría no existe"
                )

        for field, value in update_data.items():
            setattr(db_transaction, field, value)

        db.commit()

        return db.query(models.Transaction).options(
            joinedload(models.Transaction.category)
        ).filter(models.Transaction.id == transaction_id).first()

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ ERROR update transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int, 
    request: Request, 
    db: Session = Depends(get_db)
):
    account = request.state.account

    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.account_id == account.id
    ).first()

    if not db_transaction:
        raise HTTPException(status_code=404, detail="No existe la transacción")

    db.delete(db_transaction)
    db.commit()
    return {"message": "Eliminada correctamente"}