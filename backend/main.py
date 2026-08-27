from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 
from fastapi.security import APIKeyHeader
import models
from database import engine, SessionLocal, get_db
from routers import categories, transactions, stats, accounts  # <-- 1. Importamos accounts
from fastapi.openapi.utils import get_openapi

# 1. Creación de tablas automática
models.Base.metadata.create_all(bind=engine)

# 2. Definimos el esquema de seguridad
api_key_header = APIKeyHeader(name="X-Kaira-PIN", auto_error=False)

# 3. CREAMOS LA APP
app = FastAPI(
    title="Kaira Wallet API",
    description="API de gestión de gastos con protección por PIN multicuenta",
    version="2.3.0",
)

# Rutas exentas del middleware de PIN
EXEMPT_PATHS = [
    "/api/health", "/health", 
    "/api/docs", "/docs", 
    "/api/openapi.json", "/openapi.json", 
    "/api/redoc", "/redoc", 
    "/favicon.ico",
    "/api/accounts/verify-pin"  # <-- 2. Eximimos la verificación de PIN para permitir el login inicial
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

# --- MIDDLEWARE DEL PIN DINÁMICO (CONTRA BD) ---
@app.middleware("http")
async def verify_pin(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    path = request.url.path
    
    # Comprobar si la ruta actual está exenta
    if path.rstrip("/") in [p.rstrip("/") for p in EXEMPT_PATHS] or path.startswith("/docs") or path.startswith("/api/docs"):
        return await call_next(request)

    # Leemos el PIN de los headers
    user_pin = request.headers.get("X-Kaira-PIN") or request.headers.get("x-kaira-pin")
    
    if not user_pin:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "PIN de acceso no proporcionado"}
        )

    # 3. Validamos el PIN contra las cuentas registradas en la Base de Datos
    db = SessionLocal()
    try:
        account = db.query(models.Account).filter(models.Account.pin_code == user_pin).first()
        if not account:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "PIN de acceso inválido"}
            )
        # Inyectamos la cuenta encontrada en el estado de la petición para usarla en los routers
        request.state.account = account
    finally:
        db.close()
    
    return await call_next(request)

# 4. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. REGISTRO DE ROUTERS
app.include_router(categories.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(accounts.router, prefix="/api")  # <-- Incluimos las rutas de cuentas

# 6. Eventos de sistema e inicialización
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    try:
        init_default_user(db)
        init_default_accounts(db)  # <-- Inicializamos cuentas base
        init_predefined_categories(db)
        print("✅ Base de datos inicializada - Sistema Multicuenta por PIN activo")
    except Exception as e:
        print(f"⚠️ Error en startup: {e}")
    finally:
        db.close()

@app.get("/health", tags=["System"])
@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "online", "protection": "PIN_MULTIACCOUNT_ENABLED"}

# --- FUNCIONES DE INICIALIZACIÓN ---

def init_default_user(db):
    existing_user = db.query(models.User).filter(models.User.id == 1).first()
    if not existing_user:
        default_user = models.User(
            id=1,
            email="user@kaira.local",
            hashed_password="dummy_password"
        )
        db.add(default_user)
        db.commit()

def init_default_accounts(db):
    """Crea las cuentas Personal y Conjunta si no existen"""
    personal = db.query(models.Account).filter(models.Account.pin_code == "8825").first()
    if not personal:
        db.add(models.Account(name="Personal Eloy", is_joint=False, pin_code="8825"))
        
    joint = db.query(models.Account).filter(models.Account.pin_code == "1711").first()
    if not joint:
        db.add(models.Account(name="Cuenta Conjunta", is_joint=True, pin_code="1711"))
        
    db.commit()

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
                user_id=None
            )
            db.add(category)
    db.commit()
    
#             uvicorn main:app --host 0.0.0.0 --port 8000 --reload
