from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from datetime import datetime

from app.models.eventos import Evento, ParticipanteEvento
from app.schemas.eventos import EventoCreate, EventoUpdate
from app.repositories.tipos_evento_repository import TiposEventoRepository
from app.repositories.estados_evento_repository import EstadosEventoRepository


class EventosRepository:
    def __init__(self, db: Session):
        self.db = db
        self.tipos_repo = TiposEventoRepository(db)
        self.estados_repo = EstadosEventoRepository(db)
    
    def create(self, evento_data: EventoCreate) -> Evento:
        """Crear nuevo evento"""
        tipo = self.tipos_repo.get_by_codigo(evento_data.tipo_codigo)
        estado = self.estados_repo.get_estado_inicial()
        
        db_evento = Evento(
            nombre=evento_data.nombre,
            descripcion=evento_data.descripcion,
            tipo_id=tipo.id,
            lugar=evento_data.lugar,
            fecha_presentacion=evento_data.fecha_presentacion,
            estado_id=estado.id,
            creado_por=evento_data.creado_por
        )
        
        self.db.add(db_evento)
        self.db.commit()
        self.db.refresh(db_evento)
        return db_evento
    
    def get_by_id(self, evento_id: UUID) -> Optional[Evento]:
        """Obtener evento por ID"""
        return self.db.query(Evento).options(
            joinedload(Evento.tipo),
            joinedload(Evento.estado),
            joinedload(Evento.participantes).joinedload(ParticipanteEvento.estado)
        ).filter(
            and_(Evento.id == evento_id, Evento.eliminado_en.is_(None))
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Evento]:
        """Obtener lista de eventos"""
        return self.db.query(Evento).options(
            joinedload(Evento.tipo),
            joinedload(Evento.estado)
        ).filter(
            Evento.eliminado_en.is_(None)
        ).offset(skip).limit(limit).all()
    
    def update(self, evento_id: UUID, evento_data: EventoUpdate) -> Optional[Evento]:
        """Actualizar evento"""
        db_evento = self.get_by_id(evento_id)
        if not db_evento:
            return None
        
        update_data = evento_data.model_dump(exclude_unset=True)
        
        # Manejar cambio de tipo
        if "tipo_codigo" in update_data:
            tipo = self.tipos_repo.get_by_codigo(update_data.pop("tipo_codigo"))
            update_data["tipo_id"] = tipo.id
        
        # Manejar cambio de estado
        if "estado_codigo" in update_data:
            estado = self.estados_repo.get_by_codigo(update_data.pop("estado_codigo"))
            update_data["estado_id"] = estado.id
        
        for field, value in update_data.items():
            setattr(db_evento, field, value)
        
        self.db.commit()
        self.db.refresh(db_evento)
        return db_evento
    
    def delete(self, evento_id: UUID) -> bool:
        """Eliminar evento (soft delete)"""
        db_evento = self.get_by_id(evento_id)
        if not db_evento:
            return False
        
        db_evento.eliminado_en = datetime.utcnow()
        self.db.commit()
        return True
    
    def count(self) -> int:
        """Contar total de eventos activos"""
        return self.db.query(Evento).filter(
            Evento.eliminado_en.is_(None)
        ).count()
    
    def get_by_tipo(self, tipo_id: int, skip: int = 0, limit: int = 100) -> List[Evento]:
        """Obtener eventos por tipo"""
        return self.db.query(Evento).options(
            joinedload(Evento.tipo),
            joinedload(Evento.estado)
        ).filter(
            and_(
                Evento.tipo_id == tipo_id,
                Evento.eliminado_en.is_(None)
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_estado(self, estado_id: int, skip: int = 0, limit: int = 100) -> List[Evento]:
        """Obtener eventos por estado"""
        return self.db.query(Evento).options(
            joinedload(Evento.tipo),
            joinedload(Evento.estado)
        ).filter(
            and_(
                Evento.estado_id == estado_id,
                Evento.eliminado_en.is_(None)
            )
        ).offset(skip).limit(limit).all()