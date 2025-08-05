from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from app.models.eventos import ParticipanteEvento
from app.schemas.eventos import ParticipanteEventoCreate, ParticipanteEventoUpdate
from app.repositories.estados_participante_repository import EstadosParticipanteRepository


class ParticipantesEventoRepository:
    def __init__(self, db: Session):
        self.db = db
        self.estados_repo = EstadosParticipanteRepository(db)
    
    def create(self, evento_id: UUID, participante_data: ParticipanteEventoCreate) -> ParticipanteEvento:
        """Crear participante de evento"""
        estado = self.estados_repo.get_by_codigo(participante_data.estado_codigo)
        
        db_participante = ParticipanteEvento(
            evento_id=evento_id,
            musico_id=participante_data.musico_id,
            estado_id=estado.id
        )
        
        self.db.add(db_participante)
        self.db.commit()
        self.db.refresh(db_participante)
        return db_participante

    def get_by_evento_and_musico(self, evento_id: UUID, musico_id: UUID) -> Optional[ParticipanteEvento]:
        """Obtener participante específico"""
        return self.db.query(ParticipanteEvento).options(
            joinedload(ParticipanteEvento.estado)
        ).filter(
            and_(
                ParticipanteEvento.evento_id == evento_id,
                ParticipanteEvento.musico_id == musico_id
            )
        ).first()

    def update(self, evento_id: UUID, musico_id: UUID, participante_data: ParticipanteEventoUpdate) -> Optional[ParticipanteEvento]:
        """Actualizar participante de evento"""
        db_participante = self.get_by_evento_and_musico(evento_id, musico_id)
        if not db_participante:
            return None
        
        estado = self.estados_repo.get_by_codigo(participante_data.estado_codigo)
        
        db_participante.estado_id = estado.id
        self.db.commit()
        self.db.refresh(db_participante)
        return db_participante

    def get_by_evento(self, evento_id: UUID) -> List[ParticipanteEvento]:
        """Obtener todos los participantes de un evento"""
        return self.db.query(ParticipanteEvento).options(
            joinedload(ParticipanteEvento.estado)
        ).filter(
            ParticipanteEvento.evento_id == evento_id
        ).all()
    
    def count_by_evento(self, evento_id: UUID) -> int:
        """Contar participantes de un evento"""
        return self.db.query(ParticipanteEvento).filter(
            ParticipanteEvento.evento_id == evento_id
        ).count()
    
    def delete(self, evento_id: UUID, musico_id: UUID) -> bool:
        """Eliminar participante de evento"""
        db_participante = self.get_by_evento_and_musico(evento_id, musico_id)
        if not db_participante:
            return False
        
        self.db.delete(db_participante)
        self.db.commit()
        return True
