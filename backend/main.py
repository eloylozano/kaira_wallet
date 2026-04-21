from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, get_db
from routers import categories, transactions, stats

# --- CONFIGURACIÓN DE SEGURIDAD ---
ACCESS_PIN = "8061" 
EXEMPT_PATHS = ["/health", "/docs", "/openapi.json"] # Rutas que no requieren PIN

# 1. Creación de tablas automática
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kaira Wallet API",
    description="API de gestión de gastos con protección por PIN",
    version="2.2.0"
)

# 2. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. MIDDLEWARE DE PIN (El "Portero") ---
@app.middleware("http")
async def verify_pin(request: Request, call_next):
    # Si la ruta es pública (como el health check), la dejamos pasar
    if request.url.path in EXEMPT_PATHS:
        return await call_next(request)
    
    # Buscamos el PIN en los headers de la petición
    user_pin = request.headers.get("X-Kaira-PIN")
    
    if user_pin != ACCESS_PIN:
        return await request.app.middleware_stack.build_response(
            request, 
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="PIN de acceso inválido o no proporcionado"
            )
        )
    
    return await call_next(request)

# 4. Registro de Routers
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(stats.router)

# 5. Eventos de sistema
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    try:
        init_predefined_categories(db)
        print("✅ Categorías inicializadas y API protegida por PIN")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        db.close()

# 6. Health Check
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "online", "protection": "PIN_ENABLED"}

# 7. Lógica de inicialización de categorías
def init_predefined_categories(db):
    predefined = [
        ("Transporte", "Gastos de movilidad", models.TransactionType.expense, None),
        ("Coche", "Gastos del automóvil", models.TransactionType.expense, 1),
        ("Gasolina", "Combustible", models.TransactionType.expense, 1),
        ("Alimentación", "Comida", models.TransactionType.expense, None),
        ("Supermercado", "Compras", models.TransactionType.expense, 4),
        ("Restaurante", "Comidas fuera", models.TransactionType.expense, 4),
        ("Vivienda", "Gastos de casa", models.TransactionType.expense, None),
        ("Alquiler", "Pago mensual", models.TransactionType.expense, 7),
        ("Ocio", "Diversión", models.TransactionType.expense, None),
        ("Salario", "Ingresos laborales", models.TransactionType.income, None),
        ("Freelance", "Trabajos extra", models.TransactionType.income, None),
        ("Inversiones", "Dinero invertido", models.TransactionType.invest, None),
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