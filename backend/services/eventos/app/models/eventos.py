from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Evento(Base):
    __tablename__ = "eventos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    tipo_id = Column(Integer, ForeignKey("cat_tipos_evento.id"), nullable=False)
    lugar = Column(String(255))
    fecha_presentacion = Column(DateTime(timezone=True), nullable=False)
    estado_id = Column(Integer, ForeignKey("cat_estados_evento.id"), nullable=False)
    creado_por = Column(UUID(as_uuid=True), nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    eliminado_en = Column(DateTime(timezone=True))
    
    # Relationships
    tipo = relationship("CatTiposEvento")
    estado = relationship("CatEstadosEvento")
    participantes = relationship("ParticipanteEvento", back_populates="evento")

class ParticipanteEvento(Base):
    __tablename__ = "participantes_evento"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    evento_id = Column(UUID(as_uuid=True), ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False)
    musico_id = Column(UUID(as_uuid=True), nullable=False)  # Sin FK - referencia externa
    estado_id = Column(Integer, ForeignKey("cat_estados_participante.id"), nullable=False)
    unido_en = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    evento = relationship("Evento", back_populates="participantes")
    estado = relationship("CatEstadosParticipante")