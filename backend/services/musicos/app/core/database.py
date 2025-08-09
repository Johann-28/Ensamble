from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Crear engine con configuración para PostgreSQL
engine = create_engine(
    settings.get_database_url(),
    pool_pre_ping=True,
    echo=settings.debug,
    connect_args={
        "options": f"-csearch_path={settings.database_schema}"
    }
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para modelos
Base = declarative_base()

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error en sesión de base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_connection():
    """Función para verificar la conexión a la base de datos"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Conexión a base de datos exitosa")
            return True
    except Exception as e:
        logger.error(f"Error conectando a base de datos: {e}")
        return False