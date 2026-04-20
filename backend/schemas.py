from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import enum

class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"
    invest = "invest"

class FrequencyType(enum.Enum):
    fixed = "fixed"
    variable = "variable"

# ===== CATEGORÍAS =====

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    transaction_type: TransactionType
    parent_id: Optional[int] = None  # Para subcategorías

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    is_predefined: bool
    user_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryWithSubcategories(Category):
    """Categoría con sus subcategorías incluidas"""
    subcategories: List['Category'] = []
    
    class Config:
        from_attributes = True

# ===== TRANSACCIONES =====

class TransactionBase(BaseModel):
    type: TransactionType
    amount: float
    description: Optional[str] = None
    category_id: int
    notes: Optional[str] = None
    frequency: FrequencyType = FrequencyType.variable

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    notes: Optional[str] = None
    frequency: Optional[FrequencyType] = None
    date: Optional[datetime] = None

class Transaction(TransactionBase):
    id: int
    date: datetime
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TransactionWithCategory(Transaction):
    """Transacción con información de la categoría"""
    category: Category
    
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
    total_income: float
    total_expense: float
    total_invest: float
    fixed_transactions: int
    variable_transactions: int