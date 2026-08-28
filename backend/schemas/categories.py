from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .enums import TransactionType

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
    order: Optional[int] = 0

class CategoryReorderItem(BaseModel):
    id: int
    order: int

class CategoryBatchReorder(BaseModel):
    items: List[CategoryReorderItem]

class Category(CategoryBase):
    id: int
    is_predefined: bool
    user_id: Optional[int]
    created_at: datetime
    order: Optional[int] = 0

    class Config:
        from_attributes = True

class CategoryWithSubcategories(Category):
    subcategories: List['Category'] = Field(default_factory=list)
    
    class Config:
        from_attributes = True