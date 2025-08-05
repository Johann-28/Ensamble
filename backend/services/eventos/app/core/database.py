from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Crear engine con search_path configurado
engine = create_engine(
    settings.database_url,
    connect_args={
        "options": f"-c search_path={settings.database_schema},public"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos con schema específico
metadata = MetaData(schema=settings.database_schema)
Base = declarative_base(metadata=metadata)

# Dependency para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()