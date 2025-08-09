from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.musicos_service import MusicosService
from app.schemas.musicos import (
    MusicoCreate, MusicoUpdate, MusicoResponse, MusicosListResponse,
    EstadoMusicoResponse
)

router = APIRouter()

def get_musicos_service(db: Session = Depends(get_db)) -> MusicosService:
    return MusicosService(db)

# ==================== ENDPOINTS DE MÚSICOS ====================

@router.post("/", response_model=MusicoResponse, status_code=status.HTTP_201_CREATED)
async def create_musico(
    musico_data: MusicoCreate,
    service: MusicosService = Depends(get_musicos_service)
):
    """Crear un nuevo músico"""
    return service.create_musico(musico_data)

@router.get("/", response_model=MusicosListResponse)
async def get_musicos(
    skip: int = Query(0, ge=0, description="Elementos a omitir"),
    limit: int = Query(20, ge=1, le=100, description="Elementos por página"),
    activos_solo: bool = Query(True, description="Solo músicos activos"),
    service: MusicosService = Depends(get_musicos_service)
):
    """Obtener lista de músicos con paginación"""
    musicos, total = service.get_musicos(skip=skip, limit=limit, activos_solo=activos_solo)
    
    return MusicosListResponse(
        musicos=musicos,
        total=total,
        page=(skip // limit) + 1,
        size=len(musicos)
    )

@router.get("/search", response_model=List[MusicoResponse])
async def search_musicos(
    nombre: str = Query(..., min_length=1, description="Nombre a buscar"),
    skip: int = Query(0, ge=0, description="Elementos a omitir"),
    limit: int = Query(20, ge=1, le=100, description="Elementos por página"),
    service: MusicosService = Depends(get_musicos_service)
):
    """Buscar músicos por nombre"""
    return service.search_musicos(nombre, skip=skip, limit=limit)

@router.get("/{musico_id}", response_model=MusicoResponse)
async def get_musico(
    musico_id: UUID,
    service: MusicosService = Depends(get_musicos_service)
):
    """Obtener un músico específico por ID"""
    return service.get_musico(musico_id)

@router.put("/{musico_id}", response_model=MusicoResponse)
async def update_musico(
    musico_id: UUID,
    musico_data: MusicoUpdate,
    service: MusicosService = Depends(get_musicos_service)
):
    """Actualizar un músico existente"""
    return service.update_musico(musico_id, musico_data)

@router.delete("/{musico_id}", status_code=status.HTTP_200_OK)
async def delete_musico(
    musico_id: UUID,
    service: MusicosService = Depends(get_musicos_service)
):
    """Eliminar un músico (soft delete)"""
    return service.delete_musico(musico_id)

# ==================== ENDPOINTS DE CATÁLOGOS ====================

@router.get("/catalogs/estados-musico", response_model=List[EstadoMusicoResponse])
async def get_estados_musico(
    service: MusicosService = Depends(get_musicos_service)
):
    """Obtener catálogo de estados de músico"""
    return service.get_estados_musico()

