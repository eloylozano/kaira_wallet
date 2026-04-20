import enum
from sqlalchemy import Column, Enum, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
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
    
    # Relaciones
    categories = relationship("Category", back_populates="user", foreign_keys="Category.user_id")
    transactions = relationship("Transaction", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    # Tipo de transacción a la que pertenece esta categoría
    transaction_type = Column(Enum(TransactionType), nullable=False)
    
    # Relación jerárquica para subcategorías
    # Ej: parent_id = 1 (Transporte) -> esto es una subcategoría
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    
    # Para diferenciar categorías predefinidas de personalizadas
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NULL = predefinida
    is_predefined = Column(Boolean, default=False)
    
    # Relaciones
    user = relationship("User", back_populates="categories", foreign_keys=[user_id])
    transactions = relationship("Transaction", back_populates="category")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos principales
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Categorización
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    # Información adicional
    description = Column(String, nullable=True)
    notes = Column(Text, nullable=True)  # Comentarios/notas detalladas
    
    # Tipo de periodicidad (fijo o variable)
    frequency = Column(Enum(FrequencyType), default=FrequencyType.variable)
    
    # Metadatos
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")