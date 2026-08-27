from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class AccountBase(BaseModel):
    name: str
    is_joint: bool = False
    description: Optional[str] = None  # <--- Añadido aquí

class AccountCreate(AccountBase):
    pin_code: Optional[str] = None
    monthly_budget: Optional[float] = None
    inv_target: Optional[float] = None
    inv_rules: Optional[Any] = None
    inv_colors: Optional[Any] = None

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None  # <--- Añadido aquí
    is_joint: Optional[bool] = None
    pin_code: Optional[str] = None
    monthly_budget: Optional[float] = None
    inv_target: Optional[float] = None
    inv_rules: Optional[Any] = None
    inv_colors: Optional[Any] = None

class Account(AccountBase):
    id: int
    created_at: datetime
    monthly_budget: Optional[float] = None
    inv_target: Optional[float] = None
    inv_rules: Optional[Any] = None
    inv_colors: Optional[Any] = None

    class Config:
        from_attributes = True