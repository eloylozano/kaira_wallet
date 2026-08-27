from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Account
from schemas.accounts import Account as AccountResponse, AccountCreate, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/", response_model=List[AccountResponse])
def get_accounts(
    x_kaira_pin: Optional[str] = Header(None), 
    db: Session = Depends(get_db)
):
    if x_kaira_pin:
        accounts = db.query(Account).filter(Account.pin_code == x_kaira_pin).all()
        if accounts:
            return accounts
    return db.query(Account).all()

# NUEVO: Endpoint para actualizar la cuenta activa mediante el PIN de la cabecera
@router.patch("/me", response_model=AccountResponse)
def update_my_account(
    account_data: AccountUpdate,
    x_kaira_pin: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    if not x_kaira_pin:
        raise HTTPException(status_code=401, detail="PIN no proporcionado")
    
    account = db.query(Account).filter(Account.pin_code == x_kaira_pin).first()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada para este PIN")

    update_dict = account_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(account, key, value)

    db.commit()
    db.refresh(account)
    return account

@router.get("/me", response_model=AccountResponse)
def get_my_account(
    x_kaira_pin: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    if not x_kaira_pin:
        raise HTTPException(status_code=401, detail="PIN no proporcionado")
    
    account = db.query(Account).filter(Account.pin_code == x_kaira_pin).first()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada para este PIN")
    
    return account

@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int, 
    account_data: AccountUpdate, 
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    update_dict = account_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(account, key, value)

    db.commit()
    db.refresh(account)
    return account