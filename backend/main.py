from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db

# Crear tablas automáticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="App de Gastos PWA",
    description="API para gestionar gastos personales de forma escalable",
    version="2.0.0"
)

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambiar a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== FUNCIONES AUXILIARES =====

def init_predefined_categories(db: Session):
    """Inicializa categorías predefinidas en la BD"""
    predefined = [
        # GASTOS - Transporte
        ("Transporte", "Categoría padre para gastos de transporte", models.TransactionType.expense, None),
        ("Coche", "Gastos del automóvil", models.TransactionType.expense, 1),
        ("Moto", "Gastos de moto", models.TransactionType.expense, 1),
        ("Recambios", "Repuestos y accesorios", models.TransactionType.expense, 1),
        ("Gasolina", "Combustible", models.TransactionType.expense, 1),
        
        # GASTOS - Alimentación
        ("Alimentación", "Categoría padre para gastos de comida", models.TransactionType.expense, None),
        ("Supermercado", "Compras de supermercado", models.TransactionType.expense, 6),
        ("Restaurante", "Comidas fuera de casa", models.TransactionType.expense, 6),
        
        # GASTOS - Vivienda
        ("Vivienda", "Categoría padre para gastos de casa", models.TransactionType.expense, None),
        ("Alquiler", "Pago de alquiler", models.TransactionType.expense, 9),
        ("Servicios", "Agua, luz, internet", models.TransactionType.expense, 9),
        ("Mantenimiento", "Reparaciones y limpieza", models.TransactionType.expense, 9),
        
        # GASTOS - Ocio
        ("Ocio", "Entretenimiento y diversión", models.TransactionType.expense, None),
        ("Cine", "Películas y entretenimiento", models.TransactionType.expense, 13),
        ("Suscripciones", "Netflix, Spotify, etc", models.TransactionType.expense, 13),
        
        # INGRESOS
        ("Salario", "Ingresos laborales", models.TransactionType.income, None),
        ("Freelance", "Trabajos puntuales", models.TransactionType.income, None),
        ("Otros Ingresos", "Ingresos diversos", models.TransactionType.income, None),
        
        # INVERSIONES
        ("Inversiones", "Dinero invertido", models.TransactionType.invest, None),
        ("Bolsa", "Inversión en acciones", models.TransactionType.invest, 19),
        ("Criptomonedas", "Inversión en cripto", models.TransactionType.invest, 19),
    ]
    
    for name, description, trans_type, parent_id in predefined:
        exists = db.query(models.Category).filter(
            models.Category.name == name,
            models.Category.is_predefined == True
        ).first()
        if not exists:
            category = models.Category(
                name=name,
                description=description,
                transaction_type=trans_type,
                parent_id=parent_id,
                is_predefined=True
            )
            db.add(category)
    
    db.commit()

# Inicializar categorías al arrancar
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    init_predefined_categories(db)
    db.close()

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.0.0"}

# ===== ENDPOINTS PARA CATEGORÍAS =====

@app.get("/categories/predefined", response_model=List[schemas.CategoryWithSubcategories])
def get_predefined_categories(transaction_type: schemas.TransactionType = None, db: Session = Depends(get_db)):
    """Obtiene categorías predefinidas, opcionalmente filtradas por tipo de transacción"""
    query = db.query(models.Category).filter(
        models.Category.is_predefined == True,
        models.Category.parent_id == None  # Solo categorías padre
    )
    
    if transaction_type:
        query = query.filter(models.Category.transaction_type == transaction_type)
    
    return query.all()

@app.post("/categories/", response_model=schemas.Category)
def create_custom_category(
    category: schemas.CategoryCreate,
    user_id: int,  # En el futuro, obtener del JWT
    db: Session = Depends(get_db)
):
    """Crea una categoría personalizada para un usuario"""
    # Validar que el parent_id existe (si se especifica)
    if category.parent_id:
        parent = db.query(models.Category).filter(models.Category.id == category.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Categoría padre no encontrada")
    
    db_category = models.Category(
        **category.model_dump(),
        user_id=user_id,
        is_predefined=False
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[schemas.CategoryWithSubcategories])
def get_all_categories(
    user_id: int,
    transaction_type: schemas.TransactionType = None,
    db: Session = Depends(get_db)
):
    """Obtiene categorías (predefinidas + personalizadas del usuario)"""
    query = db.query(models.Category).filter(
        models.Category.parent_id == None,
        ((models.Category.is_predefined == True) | (models.Category.user_id == user_id))
    )
    
    if transaction_type:
        query = query.filter(models.Category.transaction_type == transaction_type)
    
    return query.all()

@app.get("/categories/{category_id}", response_model=schemas.CategoryWithSubcategories)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Obtiene una categoría con sus subcategorías"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, user_id: int, db: Session = Depends(get_db)):
    """Elimina una categoría personalizada (no se pueden eliminar predefinidas)"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    if category.is_predefined:
        raise HTTPException(status_code=403, detail="No se pueden eliminar categorías predefinidas")
    
    if category.user_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta categoría")
    
    db.delete(category)
    db.commit()
    return {"message": "Categoría eliminada"}

# ===== ENDPOINTS PARA TRANSACCIONES =====

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Crea una nueva transacción"""
    # Validar que la categoría existe y pertenece al usuario o es predefinida
    category = db.query(models.Category).filter(models.Category.id == transaction.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Validar que el tipo de transacción coincide con la categoría
    if category.transaction_type != transaction.type:
        raise HTTPException(
            status_code=400,
            detail=f"La transacción debe ser de tipo {category.transaction_type.value}"
        )
    
    db_transaction = models.Transaction(
        **transaction.model_dump(),
        user_id=user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=List[schemas.TransactionWithCategory])
def get_transactions(
    user_id: int,
    frequency: schemas.FrequencyType = None,
    transaction_type: schemas.TransactionType = None,
    db: Session = Depends(get_db)
):
    """Obtiene transacciones del usuario con filtros opcionales"""
    query = db.query(models.Transaction).filter(models.Transaction.user_id == user_id)
    
    if frequency:
        query = query.filter(models.Transaction.frequency == frequency)
    
    if transaction_type:
        query = query.filter(models.Transaction.type == transaction_type)
    
    return query.order_by(models.Transaction.date.desc()).all()

@app.get("/transactions/{transaction_id}", response_model=schemas.TransactionWithCategory)
def get_transaction(transaction_id: int, user_id: int, db: Session = Depends(get_db)):
    """Obtiene una transacción específica"""
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    return transaction

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Actualiza una transacción"""
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    # Validar nueva categoría si se especifica
    if transaction_update.category_id:
        category = db.query(models.Category).filter(
            models.Category.id == transaction_update.category_id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Actualizar solo los campos proporcionados
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)
    
    db.commit()
    db.refresh(transaction)
    return transaction

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, user_id: int, db: Session = Depends(get_db)):
    """Elimina una transacción"""
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    db.delete(transaction)
    db.commit()
    return {"message": "Transacción eliminada"}

# ===== ENDPOINTS PARA ESTADÍSTICAS =====

@app.get("/stats/", response_model=schemas.TransactionStatsResponse)
def get_stats(user_id: int, db: Session = Depends(get_db)):
    """Obtiene estadísticas de transacciones del usuario"""
    from sqlalchemy import func
    
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
    
    total_income = sum(t.amount for t in transactions if t.type == models.TransactionType.income)
    total_expense = sum(t.amount for t in transactions if t.type == models.TransactionType.expense)
    total_invest = sum(t.amount for t in transactions if t.type == models.TransactionType.invest)
    
    fixed_count = len([t for t in transactions if t.frequency == models.FrequencyType.fixed])
    variable_count = len([t for t in transactions if t.frequency == models.FrequencyType.variable])
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "total_invest": total_invest,
        "fixed_transactions": fixed_count,
        "variable_transactions": variable_count
    }

@app.get("/stats/by-category/")
def get_stats_by_category(user_id: int, transaction_type: schemas.TransactionType, db: Session = Depends(get_db)):
    """Obtiene gastos agrupados por categoría"""
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.type == transaction_type
    ).all()
    
    stats = {}
    for transaction in transactions:
        category_name = transaction.category.name
        stats[category_name] = stats.get(category_name, 0) + transaction.amount
    
    return stats