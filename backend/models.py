import enum
from sqlalchemy import (
    Column,
    Enum as SQLEnum,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
    Float,
    Table,
    JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# --- ENUMS ---
class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"
    invest = "invest"

class FrequencyType(enum.Enum):
    fixed = "fixed"
    variable = "variable"


# --- TABLA INTERMEDIA USUARIOS <-> CUENTAS ---
user_accounts = Table(
    'user_accounts',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('account_id', Integer, ForeignKey('accounts.id'), primary_key=True)
)


# --- MODELO CUENTA / PERFIL ---
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_joint = Column(Boolean, default=False)
    pin_code = Column(String, nullable=True, index=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Configuración propia de cada cuenta
    monthly_budget = Column(Float, default=0.0, nullable=False)
    inv_target = Column(Float, default=0.0, nullable=False)
    inv_rules = Column(JSON, default=dict, nullable=False)
    inv_colors = Column(JSON, default=dict, nullable=False)

    # Relaciones
    users = relationship("User", secondary=user_accounts, back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="account")
    budgets = relationship("MonthlyBudget", back_populates="account")


# --- MODELO USUARIO ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    accounts = relationship("Account", secondary=user_accounts, back_populates="users")
    categories = relationship("Category", back_populates="user", foreign_keys="Category.user_id")
    transactions = relationship("Transaction", back_populates="user")


# --- MODELO CATEGORÍA ---
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
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    is_predefined = Column(Boolean, default=False)
    icon = Column(String, nullable=True)

    user = relationship("User", back_populates="categories", foreign_keys=[user_id])
    account = relationship("Account", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# --- MODELO TRANSACCIÓN ---
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    type = Column(SQLEnum(TransactionType), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    date = Column(DateTime(timezone=True), nullable=True, server_default=func.now())

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    description = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    is_paid = Column(Boolean, default=True, nullable=False)
    frequency = Column(SQLEnum(FrequencyType), default=FrequencyType.variable)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


# --- MODELO PRESUPUESTO MENSUAL ---
class MonthlyBudget(Base):
    __tablename__ = "monthly_budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True, index=True)

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

    account = relationship("Account", back_populates="budgets")