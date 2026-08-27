from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .enums import TransactionType, FrequencyType, CurrencyCode, Currency
from .categories import Category

class TransactionBase(BaseModel):
    type: TransactionType
    amount: Currency
    currency: CurrencyCode = CurrencyCode.EUR
    description: Optional[str] = None
    category_id: int
    account_id: Optional[int] = None 
    notes: Optional[str] = None
    date: Optional[datetime] = None
    frequency: FrequencyType = FrequencyType.variable
    is_paid: bool = True

class TransactionUpdate(BaseModel):
    type: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    category_id: Optional[int] = None
    account_id: Optional[int] = None
    is_paid: Optional[bool] = None
    frequency: Optional[str] = None
    user_id: Optional[int] = None
    currency: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    date: datetime
    account_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TransactionWithCategory(Transaction):
    category: Optional[Category] = None
    
    class Config:
        from_attributes = True
