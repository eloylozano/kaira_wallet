from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from pydantic import EmailStr
import models, schemas, auth_utils
from database import engine, get_db

# Crear tablas automáticamente
# try:
#     models.Base.metadata.create_all(bind=engine)
# except Exception as e:
#     print(f"⚠️ Error creando tablas: {e}")
#     print("Asegúrate de que PostgreSQL está corriendo y DATABASE_URL es correcta")
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Kaira Wallet")
router = APIRouter() # <--- CLAVE: Definirlo aquí arriba
# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambiar a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Excepción de credenciales
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudo validar el acceso",
    headers={"WWW-Authenticate": "Bearer"},
)

# ===== FUNCIONES AUXILIARES =====

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Obtiene el usuario actual del token JWT"""
    try:
        payload = jwt.decode(token, auth_utils.SECRET_KEY, algorithms=[auth_utils.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en BD: {str(e)}")
    
    if user is None:
        raise credentials_exception
    return user

# ===== ENDPOINTS DE AUTENTICACIÓN =====

@app.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario"""
    try:
        # Verificar si el email ya existe
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear nuevo usuario
        hashed_password = auth_utils.get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Inicializar categorías predefinidas para el usuario
        init_predefined_categories(db)
        
        return db_user
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al registrar usuario. Verifica que el email sea válido"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en base de datos: {str(e)}"
        )

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login del usuario. Retorna token JWT"""
    try:
        user = db.query(models.User).filter(models.User.email == form_data.username).first()
        if not user or not auth_utils.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = auth_utils.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en login: {str(e)}"
        )
app.include_router(router)

@app.get("/me", response_model=schemas.User)
async def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """Obtiene información del usuario actual"""
    return current_user

# ===== HEALTH CHECK =====

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.0.0"}

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
    try:
        db = next(get_db())
        init_predefined_categories(db)
        db.close()
    except Exception as e:
        print(f"⚠️ Error inicializando categorías: {e}")

# ===== ENDPOINTS DE CATEGORÍAS =====

@app.get("/categories/predefined", response_model=List[schemas.CategoryWithSubcategories])
def get_predefined_categories(transaction_type: schemas.TransactionType = None, db: Session = Depends(get_db)):
    """Obtiene categorías predefinidas, opcionalmente filtradas por tipo de transacción"""
    try:
        query = db.query(models.Category).filter(
            models.Category.is_predefined == True,
            models.Category.parent_id == None  # Solo categorías padre
        )
        
        if transaction_type:
            query = query.filter(models.Category.transaction_type == transaction_type)
        
        return query.all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categorías predefinidas: {str(e)}"
        )

@app.post("/categories/", response_model=schemas.Category)
def create_custom_category(
    category: schemas.CategoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea una categoría personalizada para el usuario actual"""
    try:
        # Validar que el parent_id existe (si se especifica)
        if category.parent_id:
            parent = db.query(models.Category).filter(models.Category.id == category.parent_id).first()
            if not parent:
                raise HTTPException(status_code=404, detail="Categoría padre no encontrada")
        
        db_category = models.Category(
            **category.model_dump(),
            user_id=current_user.id,
            is_predefined=False
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear categoría: {str(e)}"
        )

@app.get("/categories/", response_model=List[schemas.CategoryWithSubcategories])
def get_all_categories(
    current_user: models.User = Depends(get_current_user),
    transaction_type: schemas.TransactionType = None,
    db: Session = Depends(get_db)
):
    """Obtiene categorías (predefinidas + personalizadas del usuario actual)"""
    try:
        query = db.query(models.Category).filter(
            models.Category.parent_id == None,
            ((models.Category.is_predefined == True) | (models.Category.user_id == current_user.id))
        )
        
        if transaction_type:
            query = query.filter(models.Category.transaction_type == transaction_type)
        
        return query.all()
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categorías: {str(e)}"
        )

@app.get("/categories/{category_id}", response_model=schemas.CategoryWithSubcategories)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Obtiene una categoría con sus subcategorías"""
    try:
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return category
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categoría: {str(e)}"
        )

@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina una categoría personalizada (no se pueden eliminar predefinidas)"""
    try:
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        
        if not category:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        
        if category.is_predefined:
            raise HTTPException(status_code=403, detail="No se pueden eliminar categorías predefinidas")
        
        if category.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta categoría")
        
        db.delete(category)
        db.commit()
        return {"message": "Categoría eliminada"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar categoría: {str(e)}"
        )

# ===== ENDPOINTS PARA TRANSACCIONES =====

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea una nueva transacción para el usuario actual"""
    try:
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
            user_id=current_user.id
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear transacción: {str(e)}"
        )

@app.get("/transactions/", response_model=List[schemas.TransactionWithCategory])
def get_transactions(
    current_user: models.User = Depends(get_current_user),
    frequency: schemas.FrequencyType = None,
    transaction_type: schemas.TransactionType = None,
    db: Session = Depends(get_db)
):
    """Obtiene transacciones del usuario actual con filtros opcionales"""
    try:
        query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id)
        
        if frequency:
            query = query.filter(models.Transaction.frequency == frequency)
        
        if transaction_type:
            query = query.filter(models.Transaction.type == transaction_type)
        
        return query.order_by(models.Transaction.date.desc()).all()
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener transacciones: {str(e)}"
        )

@app.get("/transactions/{transaction_id}", response_model=schemas.TransactionWithCategory)
def get_transaction(
    transaction_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene una transacción específica del usuario actual"""
    try:
        transaction = db.query(models.Transaction).filter(
            models.Transaction.id == transaction_id,
            models.Transaction.user_id == current_user.id
        ).first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        
        return transaction
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener transacción: {str(e)}"
        )

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza una transacción del usuario actual"""
    try:
        transaction = db.query(models.Transaction).filter(
            models.Transaction.id == transaction_id,
            models.Transaction.user_id == current_user.id
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
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar transacción: {str(e)}"
        )

@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina una transacción del usuario actual"""
    try:
        transaction = db.query(models.Transaction).filter(
            models.Transaction.id == transaction_id,
            models.Transaction.user_id == current_user.id
        ).first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        
        db.delete(transaction)
        db.commit()
        return {"message": "Transacción eliminada"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar transacción: {str(e)}"
        )

# ===== ENDPOINTS PARA ESTADÍSTICAS =====

@app.get("/stats/", response_model=schemas.TransactionStatsResponse)
def get_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene estadísticas de transacciones del usuario actual"""
    try:
        transactions = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()
        
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
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )

@app.get("/stats/by-category/")
def get_stats_by_category(
    transaction_type: schemas.TransactionType,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene gastos agrupados por categoría del usuario actual"""
    try:
        transactions = db.query(models.Transaction).filter(
            models.Transaction.user_id == current_user.id,
            models.Transaction.type == transaction_type
        ).all()
        
        stats = {}
        for transaction in transactions:
            category_name = transaction.category.name
            stats[category_name] = stats.get(category_name, 0) + transaction.amount
        
        return stats
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas por categoría: {str(e)}"
        )

# ===== INCLUDE ROUTER =====

app.include_router(router)
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload