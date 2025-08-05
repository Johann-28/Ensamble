from sqlalchemy import Column, Integer, String, Boolean, Text
from app.core.database import Base

class CatTiposEvento(Base):
    __tablename__ = "cat_tipos_evento"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    orden = Column(Integer, default=1)

class CatEstadosEvento(Base):
    __tablename__ = "cat_estados_evento"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    orden = Column(Integer, default=1)

class CatEstadosParticipante(Base):
    __tablename__ = "cat_estados_participante"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    orden = Column(Integer, default=1)