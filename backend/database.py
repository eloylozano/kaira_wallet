from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Obtener variables de entorno
db_user = os.getenv("DB_USER", "user")
db_password = os.getenv("DB_PASSWORD", "pass")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5433")
db_name = os.getenv("DB_NAME", "kaira_wallet")

# Encoding de caracteres especiales en contraseña
db_password_encoded = quote_plus(db_password)

# Construir URL con encoding adecuado
DATABASE_URL = f"postgresql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}"

# Configurar opciones de conexión
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verificar conexión antes de usar
    echo=False  # Cambiar a True para debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()