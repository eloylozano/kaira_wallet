import enum
# 1. Importamos Enum como SQLEnum para que no choque con el enum de Python
from sqlalchemy import Column, Enum as SQLEnum, Integer, String, Numeric, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"
    invest = "invest"

class FrequencyType(enum.Enum):
    fixed = "fixed"
    variable = "variable"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    categories = relationship("Category", back_populates="user", foreign_keys="Category.user_id")
    transactions = relationship("Transaction", back_populates="user")
    
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    transaction_type = Column(SQLEnum(TransactionType), nullable=False)

    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    parent = relationship(
        "Category",
        remote_side=[id],
        back_populates="subcategories"
    )

    subcategories = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="select"
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_predefined = Column(Boolean, default=False)
    icon = Column(String, nullable=True)

    user = relationship("User", back_populates="categories", foreign_keys=[user_id])
    transactions = relationship("Transaction", back_populates="category")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    
    # 3. AQUÍ ESTABA EL ERROR: Cambia Enum por SQLEnum
    type = Column(SQLEnum(TransactionType), nullable=False)
    
    amount = Column(Numeric(12, 2), nullable=False)
    date = Column(DateTime(timezone=True), nullable=True, server_default=func.now())  # Permitir null para que el usuario lo especifique
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    description = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    is_paid = Column(Boolean, default=True, nullable=False)
    
    # 4. AQUÍ TAMBIÉN: Cambia Enum por SQLEnum
    frequency = Column(SQLEnum(FrequencyType), default=FrequencyType.variable)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")