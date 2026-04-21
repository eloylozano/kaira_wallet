from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, get_db
from routers import categories, transactions, stats

# 1. Creación de tablas automática al arrancar
# Esto lee la configuración de models.py y la aplica en la BD
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kaira Wallet API",
    description="API de gestión de gastos (Versión Simplificada)",
    version="2.1.0"
)

# 2. Configuración de CORS
# Permite que tu frontend se comunique con el backend sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Registro de Routers
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(stats.router)

# 4. Eventos de sistema
@app.on_event("startup")
def startup_event():
    """Ejecuta tareas de configuración inicial al encender el servidor"""
    db = next(get_db())
    try:
        init_predefined_categories(db)
        print("✅ Categorías inicializadas correctamente")
    except Exception as e:
        print(f"⚠️ Error al inicializar categorías: {e}")
    finally:
        db.close()

# 5. Health Check simple
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "online",
        "mode": "development_no_auth",
        "version": "2.1.0"
    }

# 6. Lógica de inicialización (Mantenida aquí o movida a utils.py)
def init_predefined_categories(db):
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

# Ejecución: uvicorn main:app --reload