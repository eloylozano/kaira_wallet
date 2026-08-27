from pydantic import BaseModel
from decimal import Decimal

class MessageResponse(BaseModel):
    message: str

class TransactionStatsResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    total_invest: Decimal
    fixed_transactions: int
    variable_transactions: int
