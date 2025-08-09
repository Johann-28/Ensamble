from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base

class Musico(Base):
    __tablename__ = "musicos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(50))
    fecha_ingreso = Column(DateTime(timezone=True), default=func.now())
    estado_id = Column(Integer, ForeignKey("cat_estados_musico.id"), nullable=False)
    url_foto_perfil = Column(Text)
    
    # Campos de auditoría
    creado_en = Column(DateTime(timezone=True), default=func.now())
    actualizado_en = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    eliminado_en = Column(DateTime(timezone=True))
    
    # Relationships
    estado = relationship("CatEstadosMusico")
    instrumentos = relationship("InstrumentoMusico", back_populates="musico")

class InstrumentoMusico(Base):
    __tablename__ = "instrumentos_musico"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    musico_id = Column(UUID(as_uuid=True), ForeignKey("musicos.id"), nullable=False)
    instrumento_id = Column(Integer, nullable=False)  # Referencia al catálogo compartido
    nivel_id = Column(Integer, nullable=False)  # Referencia al catálogo compartido
    es_principal = Column(Boolean, default=False)
    fecha_inicio = Column(Date)
    notas = Column(Text)
    
    # Relationships
    musico = relationship("Musico", back_populates="instrumentos")
    # AGREGAR ESTAS RELACIONES NUEVAS (sin foreign key por ser esquemas diferentes):
    # Las relaciones se manejan manualmente en el service layer
