from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Annotated
from decimal import Decimal
import enum

# ===== CUENTAS / WALLETS =====

class AccountBase(BaseModel):
    name: str
    is_joint: bool = False

class AccountCreate(AccountBase):
    pin_code: Optional[str] = None

class Account(AccountBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- ENUMS ---
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
    # Puedes añadir más según necesites

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
# ===== CATEGORÍAS =====

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    transaction_type: TransactionType
    parent_id: Optional[int] = None
    icon: Optional[str] = None

class CategoryCreate(BaseModel):
    name: str
    transaction_type: str
    parent_id: Optional[int] = None
    icon: Optional[str] = None

class Category(CategoryBase):
    id: int
    is_predefined: bool
    user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryWithSubcategories(Category):
    subcategories: List['Category'] = Field(default_factory=list)
    
    class Config:
        from_attributes = True

# ===== TRANSACCIONES =====

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
    account_id: Optional[int] = None  # <-- AÑADIDO
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

# ===== USUARIOS =====

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== RESPUESTAS =====

class MessageResponse(BaseModel):
    message: str

class TransactionStatsResponse(BaseModel):
    # Aquí también usamos Decimal para que los totales sean exactos
    total_income: Decimal
    total_expense: Decimal
    total_invest: Decimal
    fixed_transactions: int
    variable_transactions: int
    
# ===== BUDGET =====

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