from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from .enums import Currency

class MonthlyBudgetBase(BaseModel):
    amount: Currency
    month: int
    year: int


class MonthlyBudgetCreate(MonthlyBudgetBase):
    pass


class MonthlyBudget(MonthlyBudgetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class BudgetOverview(BaseModel):
    budget: Decimal
    spent: Decimal
    remaining: Decimal
    daily_budget: Decimal
    days_left: int
