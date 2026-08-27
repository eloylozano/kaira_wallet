from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

# 1. OBTENER TODAS LAS CUENTAS (Para verlas en Swagger)
@router.get("/", response_model=List[schemas.Account])
def get_accounts(db: Session = Depends(get_db)):
    return db.query(models.Account).all()


# 2. OBTENER UNA CUENTA POR SU ID
@router.get("/{account_id}", response_model=schemas.Account)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return account


# 3. CREAR UNA NUEVA CUENTA (Personal, Conjunta, etc.)
@router.post("/", response_model=schemas.Account, status_code=status.HTTP_201_CREATED)
def create_account(account_data: schemas.AccountCreate, db: Session = Depends(get_db)):
    new_account = models.Account(
        name=account_data.name,
        is_joint=account_data.is_joint,
        pin_code=account_data.pin_code
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


# 4. VERIFICAR PIN (El endpoint que usará tu Login/Frontend)
@router.post("/verify-pin", response_model=schemas.Account)
def verify_pin(pin: str, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.pin_code == pin).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="PIN inválido"
        )
    return account