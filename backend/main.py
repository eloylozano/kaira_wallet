from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 
from fastapi.security import APIKeyHeader
import models
from database import engine, get_db
from routers import categories, transactions, stats
from fastapi.openapi.utils import get_openapi

# 1. Creación de tablas automática
models.Base.metadata.create_all(bind=engine)

# 2. Definimos el esquema de seguridad
api_key_header = APIKeyHeader(name="X-Kaira-PIN", auto_error=False)

# 3. CREAMOS LA APP
app = FastAPI(
    title="Kaira Wallet API",
    description="API de gestión de gastos con protección por PIN",
    version="2.2.0",
)

# --- CONFIGURACIÓN DE SEGURIDAD ---
ACCESS_PIN = "8061" 

# Añadimos /api a las rutas exentas porque ahora la API vivirá bajo /api
EXEMPT_PATHS = [
    "/api/health", "/health", 
    "/api/docs", "/docs", 
    "/api/openapi.json", "/openapi.json", 
    "/api/redoc", "/redoc", 
    "/favicon.ico"
]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-Kaira-PIN"
        }
    }
    openapi_schema["security"] = [{"ApiKeyAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# --- MIDDLEWARE DEL PIN ADAPTADO ---
@app.middleware("http")
async def verify_pin(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    path = request.url.path
    
    # Toleramos tanto la versión con /api como sin ella para desarrollo local
    if path.rstrip("/") in [p.rstrip("/") for p in EXEMPT_PATHS] or path.startswith("/docs") or path.startswith("/api/docs"):
        return await call_next(request)

    # Leemos el PIN soportando tanto mayúsculas como las minúsculas que mete Nginx
    user_pin = request.headers.get("X-Kaira-PIN") or request.headers.get("x-kaira-pin")
    if user_pin != ACCESS_PIN:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "PIN de acceso inválido o no proporcionado"}
        )
    
    return await call_next(request)

# 4. Configuración de CORS (Se registra DESPUÉS del PIN para envolver los errores)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. REGISTRO DE ROUTERS CON PREFIJO GLOBAL /api
# Esto hace que todas tus rutas pasen a ser de forma nativa /api/categories, /api/stats, etc.
app.include_router(categories.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(stats.router, prefix="/api")

# 5. Eventos de sistema
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    try:
        init_default_user(db)
        init_predefined_categories(db)
        print("✅ Usuario y categorías inicializadas - API protegida por PIN")
    except Exception as e:
        print(f"⚠️ Error en startup: {e}")
    finally:
        db.close()

# 6. Health Check (Mantenemos ambos mapeos por si acaso)
@app.get("/health", tags=["System"])
@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "online", "protection": "PIN_ENABLED"}

# 7. Lógica de inicialización de categorías
def init_default_user(db):
    """Crear un usuario por defecto si no existe"""
    existing_user = db.query(models.User).filter(models.User.id == 1).first()
    if not existing_user:
        default_user = models.User(
            id=1,
            email="user@kaira.local",
            hashed_password="dummy_password"  # Solo para desarrollo
        )
        db.add(default_user)
        db.commit()
        print("✅ Usuario por defecto creado (ID: 1)")

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
                is_predefined=True,
                user_id=None  # Categorías predefinidas sin usuario específico
            )
            db.add(category)
    db.commit()
    
#             uvicorn main:app --host 0.0.0.0 --port 8000 --reload
