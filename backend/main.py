from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 
from fastapi.security import APIKeyHeader
import models
from database import engine, get_db
from routers import categories, transactions, stats

# 1. Creación de tablas automática
models.Base.metadata.create_all(bind=engine)

# 2. Definimos el esquema de seguridad
api_key_header = APIKeyHeader(name="X-Kaira-PIN", auto_error=False)

# 3. CREAMOS LA APP (Esto debe ir antes de los middlewares)
app = FastAPI(
    title="Kaira Wallet API",
    description="API de gestión de gastos con protección por PIN",
    version="2.2.0",
    dependencies=[Depends(api_key_header)] 
)

# 4. Configuración de CORS (Ahora sí, sobre 'app')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURACIÓN DE SEGURIDAD ---
ACCESS_PIN = "8061" 
EXEMPT_PATHS = ["/health", "/docs", "/openapi.json", "/favicon.ico"] 

@app.middleware("http")
async def verify_pin(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    path = request.url.path
    if path in EXEMPT_PATHS or path.startswith("/docs") or path.startswith("/openapi.json"):
        return await call_next(request)
    # Verificar el PIN
    user_pin = request.headers.get("X-Kaira-PIN")
    
    if user_pin != ACCESS_PIN:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "PIN de acceso inválido o no proporcionado"}
        )
    
    return await call_next(request)

# 5. Registro de Routers
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
    
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
