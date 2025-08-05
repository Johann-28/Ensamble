from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.eventos_service import EventosService
from app.schemas.eventos import (
    EventoCreate, EventoUpdate, EventoResponse, EventosListResponse,
    ParticipanteEventoCreate, ParticipanteEventoUpdate, ParticipanteEventoResponse,
    TipoEventoResponse
)

router = APIRouter()

def get_Eventos_service(db: Session = Depends(get_db)) -> EventosService:
    return EventosService(db)

# ==================== ENDPOINTS DE EVENTOS ====================

@router.post("/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
async def create_evento(
    evento_data: EventoCreate,
    service: EventosService = Depends(get_Eventos_service)
):
    """Crear un nuevo evento musical"""
    return service.create_evento(evento_data)

@router.get("/", response_model=EventosListResponse)
async def get_eventos(
    skip: int = Query(0, ge=0, description="Elementos a omitir"),
    limit: int = Query(20, ge=1, le=100, description="Elementos por página"),
    service: EventosService = Depends(get_Eventos_service)
):
    """Obtener lista de eventos con paginación"""
    eventos, total = service.get_eventos(skip=skip, limit=limit)
    
    return EventosListResponse(
        eventos=eventos,
        total=total,
        page=(skip // limit) + 1,
        size=len(eventos)
    )

@router.get("/{evento_id}", response_model=EventoResponse)
async def get_evento(
    evento_id: UUID,
    service: EventosService = Depends(get_Eventos_service)
):
    """Obtener un evento específico por ID"""
    return service.get_evento(evento_id)

@router.put("/{evento_id}", response_model=EventoResponse)
async def update_evento(
    evento_id: UUID,
    evento_data: EventoUpdate,
    service: EventosService = Depends(get_Eventos_service)
):
    """Actualizar un evento existente"""
    return service.update_evento(evento_id, evento_data)

@router.delete("/{evento_id}", status_code=status.HTTP_200_OK)
async def delete_evento(
    evento_id: UUID,
    service: EventosService = Depends(get_Eventos_service)
):
    """Eliminar un evento (soft delete)"""
    return service.delete_evento(evento_id)

# ==================== ENDPOINTS DE PARTICIPANTES ====================

@router.post("/{evento_id}/participantes", response_model=ParticipanteEventoResponse, status_code=status.HTTP_201_CREATED)
async def add_participante(
    evento_id: UUID,
    participante_data: ParticipanteEventoCreate,
    service: EventosService = Depends(get_Eventos_service)
):
    """Agregar un músico como participante del evento"""
    return service.add_participante(evento_id, participante_data)

@router.get("/{evento_id}/participantes", response_model=List[ParticipanteEventoResponse])
async def get_participantes_evento(
    evento_id: UUID,
    service: EventosService = Depends(get_Eventos_service)
):
    """Obtener todos los participantes de un evento"""
    return service.get_participantes_evento(evento_id)

@router.put("/{evento_id}/participantes/{musico_id}", response_model=ParticipanteEventoResponse)
async def update_participante(
    evento_id: UUID,
    musico_id: UUID,
    participante_data: ParticipanteEventoUpdate,
    service: EventosService = Depends(get_Eventos_service)
):
    """Actualizar estado de participación de un músico"""
    return service.update_participante(evento_id, musico_id, participante_data)

# ==================== ENDPOINTS DE CATÁLOGOS ====================

@router.get("/catalogs/tipos-evento", response_model=List[TipoEventoResponse])
async def get_tipos_evento(
    service: EventosService = Depends(get_Eventos_service)
):
    """Obtener catálogo de tipos de evento"""
    return service.get_tipos_evento()

@router.get("/catalogs/estados-evento", response_model=List[TipoEventoResponse])
async def get_estados_evento(
    service: EventosService = Depends(get_Eventos_service)
):
    """Obtener catálogo de estados de evento"""
    return service.get_estados_evento()

@router.get("/catalogs/estados-participante", response_model=List[TipoEventoResponse])
async def get_estados_participante(
    service: EventosService = Depends(get_Eventos_service)
):
    """Obtener catálogo de estados de participante"""
    # Implementar en el service si es necesario
    return []