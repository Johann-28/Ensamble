from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.schemas.eventos import EventoCreate, EventoUpdate, ParticipanteEventoCreate, ParticipanteEventoUpdate
from app.repositories.eventos_repository import EventosRepository
from app.repositories.tipos_evento_repository import TiposEventoRepository
from app.repositories.estados_evento_repository import EstadosEventoRepository
from app.repositories.participantes_evento_repository import ParticipantesEventoRepository
from app.repositories.estados_participante_repository import EstadosParticipanteRepository

from app.models.eventos import Evento, ParticipanteEvento
from app.models.catalogs import CatTiposEvento, CatEstadosEvento, CatEstadosParticipante


class EventosRepositoryFacade:
    """
    Repositorio principal que coordina entre los diferentes repositorios especializados
    Mantiene compatibilidad con la interfaz anterior
    """
    def __init__(self, db: Session):
        self.db = db
        self.eventos_repo = EventosRepository(db)
        self.tipos_repo = TiposEventoRepository(db)
        self.estados_repo = EstadosEventoRepository(db)
        self.participantes_repo = ParticipantesEventoRepository(db)
        self.estados_participante_repo = EstadosParticipanteRepository(db)
    
    # === Métodos de Eventos (delegados a EventosRepository) ===
    def create_evento(self, evento_data: EventoCreate) -> Evento:
        return self.eventos_repo.create(evento_data)
    
    def get_evento(self, evento_id: UUID) -> Optional[Evento]:
        return self.eventos_repo.get_by_id(evento_id)
    
    def get_eventos(self, skip: int = 0, limit: int = 100) -> List[Evento]:
        return self.eventos_repo.get_all(skip, limit)
    
    def update_evento(self, evento_id: UUID, evento_data: EventoUpdate) -> Optional[Evento]:
        return self.eventos_repo.update(evento_id, evento_data)
    
    def delete_evento(self, evento_id: UUID) -> bool:
        return self.eventos_repo.delete(evento_id)
    
    def count_eventos(self) -> int:
        return self.eventos_repo.count()
    
    # === Métodos de Catálogos ===
    def get_tipos_evento(self) -> List[CatTiposEvento]:
        return self.tipos_repo.get_all()
    
    def get_estados_evento(self) -> List[CatEstadosEvento]:
        return self.estados_repo.get_all()
    
    def get_estados_participante(self) -> List[CatEstadosParticipante]:
        return self.estados_participante_repo.get_all()
    
    # === Métodos de Participantes (delegados a ParticipantesEventoRepository) ===
    def create_participante_evento(self, evento_id: UUID, participante_data: ParticipanteEventoCreate) -> ParticipanteEvento:
        return self.participantes_repo.create(evento_id, participante_data)

    def get_participante_evento(self, evento_id: UUID, musico_id: UUID) -> Optional[ParticipanteEvento]:
        return self.participantes_repo.get_by_evento_and_musico(evento_id, musico_id)

    def update_participante_evento(self, evento_id: UUID, musico_id: UUID, participante_data: ParticipanteEventoUpdate) -> Optional[ParticipanteEvento]:
        return self.participantes_repo.update(evento_id, musico_id, participante_data)

    def get_participantes_evento(self, evento_id: UUID) -> List[ParticipanteEvento]:
        return self.participantes_repo.get_by_evento(evento_id)
    
    def delete_participante_evento(self, evento_id: UUID, musico_id: UUID) -> bool:
        return self.participantes_repo.delete(evento_id, musico_id)
    
    # === Métodos adicionales que combinan repositorios ===
    def get_eventos_by_tipo(self, tipo_codigo: str, skip: int = 0, limit: int = 100) -> List[Evento]:
        """Obtener eventos por código de tipo"""
        tipo = self.tipos_repo.get_by_codigo(tipo_codigo)
        return self.eventos_repo.get_by_tipo(tipo.id, skip, limit)
    
    def get_eventos_by_estado(self, estado_codigo: str, skip: int = 0, limit: int = 100) -> List[Evento]:
        """Obtener eventos por código de estado"""
        estado = self.estados_repo.get_by_codigo(estado_codigo)
        return self.eventos_repo.get_by_estado(estado.id, skip, limit)
