from sqlalchemy import Column, Integer, String, Boolean, Text
from app.core.database import Base

class CatEstadosMusico(Base):
    __tablename__ = "cat_estados_musico"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    orden = Column(Integer, default=1)

class CatInstrumentos(Base):
    __tablename__ = "cat_instrumentos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    familia = Column(String(50))  # viento, cuerda, percusión, etc.
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    orden = Column(Integer, default=1)
