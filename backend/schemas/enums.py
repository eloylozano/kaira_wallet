from pydantic import Field, BaseModel
from typing import Annotated, Optional
from decimal import Decimal
import enum

# Reglas comunes para moneda
Currency = Annotated[Decimal, Field(max_digits=12, decimal_places=2, gt=0)]

class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"
    invest = "invest"

class FrequencyType(str, enum.Enum):
    fixed = "fixed"
    variable = "variable"

class CurrencyCode(str, enum.Enum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
