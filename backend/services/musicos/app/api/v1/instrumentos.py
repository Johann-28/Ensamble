from fastapi import APIRouter, Depends, Query, status, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.musicos_service import MusicosService
from app.schemas.musicos import (
    InstrumentoCreate, InstrumentoMusicoCreate, InstrumentoMusicoUpdate, InstrumentoMusicoResponse,
    InstrumentoResponse, InstrumentoUpdate
)

router = APIRouter()

def get_musicos_service(db: Session = Depends(get_db)) -> MusicosService:
    return MusicosService(db)

# ==================== ENDPOINTS DE CATÁLOGOS (PRIMERO - MÁS ESPECÍFICOS) ====================

@router.get("/catalogs/familias-instrumentos", response_model=List[str])
async def get_familias_instrumentos(
    service: MusicosService = Depends(get_musicos_service)
):
    """Obtener lista de familias de instrumentos disponibles"""
    instrumentos = service.get_instrumentos_disponibles()
    familias = list(set([inst.familia for inst in instrumentos if inst.familia]))
    return sorted(familias)

@router.get("/catalogs/instrumentos", response_model=List[InstrumentoResponse])
async def get_instrumentos(
    service: MusicosService = Depends(get_musicos_service)
):
    """Obtener catálogo de instrumentos disponibles"""
    return service.get_instrumentos_disponibles()

@router.post("/catalogs/instrumentos", response_model=InstrumentoResponse, status_code=status.HTTP_201_CREATED)
async def create_instrumento(
    instrumento_data: InstrumentoCreate,
    service: MusicosService = Depends(get_musicos_service)
):
    """Crear un nuevo instrumento en el catálogo"""
    return service.create_instrumento(instrumento_data)

@router.get("/catalogs/instrumentos/{instrumento_id}", response_model=InstrumentoResponse)
async def get_instrumento_by_id(
    instrumento_id: int,
    service: MusicosService = Depends(get_musicos_service)
):
    """Obtener un instrumento específico por ID"""
    instrumento = service.catalogo_instrumentos_repo.get_by_id(instrumento_id)
    if not instrumento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrumento no encontrado"
        )
    return InstrumentoResponse.model_validate(instrumento)

@router.put("/catalogs/instrumentos/{instrumento_id}", response_model=InstrumentoResponse)
async def update_instrumento_catalog(
    instrumento_id: int,
    instrumento_data: InstrumentoUpdate,
    service: MusicosService = Depends(get_musicos_service)
):
    """Actualizar un instrumento del catálogo"""
    return service.update_instrumento_catalog(instrumento_id, instrumento_data)

@router.delete("/catalogs/instrumentos/{instrumento_id}", status_code=status.HTTP_200_OK)
async def delete_instrumento(
    instrumento_id: int,
    service: MusicosService = Depends(get_musicos_service)
):
    """Desactivar un instrumento (soft delete)"""
    return service.delete_instrumento(instrumento_id)

@router.get("/catalogs/instrumentos/familia/{familia}", response_model=List[InstrumentoResponse])
async def get_instrumentos_by_familia(
    familia: str,
    service: MusicosService = Depends(get_musicos_service)
):
    """Obtener instrumentos por familia (viento, cuerda, percusión, etc.)"""
    return service.get_instrumentos_by_familia(familia)

# ==================== ENDPOINTS DE INSTRUMENTOS DE MÚSICOS (DESPUÉS - MÁS GENÉRICOS) ====================

@router.post("/{musico_id}/instrumentos", response_model=InstrumentoMusicoResponse, status_code=status.HTTP_201_CREATED)
async def add_instrumento(
    musico_id: UUID,
    instrumento_data: InstrumentoMusicoCreate,
    service: MusicosService = Depends(get_musicos_service)
):
    """Agregar un instrumento a un músico"""
    return service.add_instrumento(musico_id, instrumento_data)

@router.get("/{musico_id}/instrumentos", response_model=List[InstrumentoMusicoResponse])
async def get_instrumentos_musico(
    musico_id: UUID,
    service: MusicosService = Depends(get_musicos_service)
):
    """Obtener todos los instrumentos de un músico"""
    return service.get_instrumentos_musico(musico_id)

@router.put("/instrumentos/{instrumento_id}", response_model=InstrumentoMusicoResponse)
async def update_instrumento_musico(
    instrumento_id: UUID,
    instrumento_data: InstrumentoMusicoUpdate,
    service: MusicosService = Depends(get_musicos_service)
):
    """Actualizar un instrumento de músico"""
    return service.update_instrumento(instrumento_id, instrumento_data)

@router.delete("/{musico_id}/instrumentos/{instrumento_id}", status_code=status.HTTP_200_OK)
async def remove_instrumento(
    musico_id: UUID,
    instrumento_id: int,
    service: MusicosService = Depends(get_musicos_service)
):
    """Eliminar un instrumento de un músico"""
    return service.remove_instrumento(musico_id, instrumento_id)