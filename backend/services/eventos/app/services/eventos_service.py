from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.eventos_repository import EventosRepository
from app.repositories.tipos_evento_repository import TiposEventoRepository
from app.repositories.estados_evento_repository import EstadosEventoRepository
from app.repositories.participantes_evento_repository import ParticipantesEventoRepository
from app.repositories.estados_participante_repository import EstadosParticipanteRepository
from app.schemas.eventos import (
    EventoCreate, EventoUpdate, EventoResponse, 
    ParticipanteEventoCreate, ParticipanteEventoUpdate,
    ParticipanteEventoResponse, TipoEventoResponse
)
from app.models.eventos import Evento, ParticipanteEvento
from app.models.catalogs import CatEstadosParticipante

class EventosService:
    def __init__(self, db: Session):
        self.db = db
        # Inicializar todos los repositorios especializados
        self.eventos_repo = EventosRepository(db)
        self.tipos_repo = TiposEventoRepository(db)
        self.estados_repo = EstadosEventoRepository(db)
        self.participantes_repo = ParticipantesEventoRepository(db)
        self.estados_participante_repo = EstadosParticipanteRepository(db)
    
    def create_evento(self, evento_data: EventoCreate) -> EventoResponse:
        """Crear un nuevo evento"""
        try:
            db_evento = self.eventos_repo.create(evento_data)
            return self._evento_to_response(db_evento)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    def get_evento(self, evento_id: UUID) -> EventoResponse:
        """Obtener un evento por ID"""
        db_evento = self.eventos_repo.get_by_id(evento_id)
        if not db_evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        return self._evento_to_response(db_evento)
    
    def get_eventos(self, skip: int = 0, limit: int = 100) -> Tuple[List[EventoResponse], int]:
        """Obtener lista de eventos con paginación"""
        if limit > 100:
            limit = 100
        
        eventos = self.eventos_repo.get_all(skip=skip, limit=limit)
        total = self.eventos_repo.count()
        
        eventos_response = [self._evento_to_response(evento) for evento in eventos]
        return eventos_response, total
    
    def update_evento(self, evento_id: UUID, evento_data: EventoUpdate) -> EventoResponse:
        """Actualizar un evento"""
        try:
            db_evento = self.eventos_repo.update(evento_id, evento_data)
            if not db_evento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Evento no encontrado"
                )
            return self._evento_to_response(db_evento)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def delete_evento(self, evento_id: UUID) -> dict:
        """Eliminar un evento (soft delete)"""
        if not self.eventos_repo.delete(evento_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        return {"message": "Evento eliminado correctamente"}
    
    def add_participante(self, evento_id: UUID, participante_data: ParticipanteEventoCreate) -> ParticipanteEventoResponse:
        """Agregar un participante al evento"""
        # Verificar que el evento existe
        evento = self.eventos_repo.get_by_id(evento_id)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        
        # Verificar si ya es participante
        existing = self.participantes_repo.get_by_evento_and_musico(evento_id, participante_data.musico_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El músico ya es participante del evento"
            )
        
        try:
            db_participante = self.participantes_repo.create(evento_id, participante_data)
            return self._participante_to_response(db_participante)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def update_participante(self, evento_id: UUID, musico_id: UUID, participante_data: ParticipanteEventoUpdate) -> ParticipanteEventoResponse:
        """Actualizar estado de un participante"""
        db_participante = self.participantes_repo.update(evento_id, musico_id, participante_data)
        if not db_participante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante no encontrado"
            )
        return self._participante_to_response(db_participante)
    
    def get_participantes_evento(self, evento_id: UUID) -> List[ParticipanteEventoResponse]:
        """Obtener todos los participantes de un evento"""
        evento = self.eventos_repo.get_by_id(evento_id)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        
        participantes = self.participantes_repo.get_by_evento(evento_id)
        return [self._participante_to_response(p) for p in participantes]
    
    def get_tipos_evento(self) -> List[TipoEventoResponse]:
        """Obtener catálogo de tipos de evento"""
        tipos = self.tipos_repo.get_all()
        return [TipoEventoResponse.model_validate(tipo) for tipo in tipos]
    
    def get_estados_evento(self) -> List[TipoEventoResponse]:
        """Obtener catálogo de estados de evento"""
        estados = self.estados_repo.get_all()
        return [TipoEventoResponse.model_validate(estado) for estado in estados]
    
    def get_estados_participante(self) -> List[TipoEventoResponse]:
        """Obtener catálogo de estados de participante"""
        estados = self.estados_participante_repo.get_all()
        return [TipoEventoResponse.model_validate(estado) for estado in estados]
    
    def remove_participante(self, evento_id: UUID, musico_id: UUID) -> dict:
        """Remover un participante del evento"""
        # Verificar que el evento existe
        evento = self.eventos_repo.get_by_id(evento_id)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        
        if not self.participantes_repo.delete(evento_id, musico_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante no encontrado"
            )
        return {"message": "Participante removido correctamente"}
    
    def get_eventos_by_tipo(self, tipo_codigo: str, skip: int = 0, limit: int = 100) -> Tuple[List[EventoResponse], int]:
        """Obtener eventos filtrados por tipo"""
        if limit > 100:
            limit = 100
        
        try:
            tipo = self.tipos_repo.get_by_codigo(tipo_codigo)
            eventos = self.eventos_repo.get_by_tipo(tipo.id, skip, limit)
            total = len(eventos)  # Para optimizar, se podría agregar un método count_by_tipo
            
            eventos_response = [self._evento_to_response(evento) for evento in eventos]
            return eventos_response, total
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def get_eventos_by_estado(self, estado_codigo: str, skip: int = 0, limit: int = 100) -> Tuple[List[EventoResponse], int]:
        """Obtener eventos filtrados por estado"""
        if limit > 100:
            limit = 100
        
        try:
            estado = self.estados_repo.get_by_codigo(estado_codigo)
            eventos = self.eventos_repo.get_by_estado(estado.id, skip, limit)
            total = len(eventos)  # Para optimizar, se podría agregar un método count_by_estado
            
            eventos_response = [self._evento_to_response(evento) for evento in eventos]
            return eventos_response, total
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def get_participante_detail(self, evento_id: UUID, musico_id: UUID) -> ParticipanteEventoResponse:
        """Obtener detalles de un participante específico"""
        # Verificar que el evento existe
        evento = self.eventos_repo.get_by_id(evento_id)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        
        participante = self.participantes_repo.get_by_evento_and_musico(evento_id, musico_id)
        if not participante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante no encontrado"
            )
        
        return self._participante_to_response(participante)
    
    def _evento_to_response(self, evento: Evento) -> EventoResponse:
        """Convertir modelo a schema de respuesta"""
        return EventoResponse.model_validate(evento)
    
    def _participante_to_response(self, participante: ParticipanteEvento) -> ParticipanteEventoResponse:
        """Convertir modelo de participante a schema de respuesta"""
        return ParticipanteEventoResponse.model_validate(participante)