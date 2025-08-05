from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# Esquemas para catálogos
class CatalogoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True
    orden: int = 1

class TipoEventoResponse(CatalogoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Esquemas para eventos
class EventoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = None
    lugar: Optional[str] = Field(None, max_length=255)
    fecha_presentacion: datetime

class EventoCreate(EventoBase):
    tipo_codigo: str
    creado_por: UUID

class EventoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    descripcion: Optional[str] = None
    lugar: Optional[str] = Field(None, max_length=255)
    fecha_presentacion: Optional[datetime] = None
    tipo_codigo: Optional[str] = None
    estado_codigo: Optional[str] = None

class EventoResponse(EventoBase):
    id: UUID
    tipo: TipoEventoResponse
    estado: TipoEventoResponse  # Reutilizamos la estructura
    creado_por: UUID
    creado_en: datetime
    actualizado_en: datetime
    eliminado_en: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# Esquemas para participantes
class ParticipanteEventoCreate(BaseModel):
    musico_id: UUID
    estado_codigo: str = "invitado"

class ParticipanteEventoUpdate(BaseModel):
    estado_codigo: str

class ParticipanteEventoResponse(BaseModel):
    id: UUID
    evento_id: UUID
    musico_id: UUID
    estado: TipoEventoResponse
    unido_en: datetime
    model_config = ConfigDict(from_attributes=True)

# Respuestas con paginación
class EventosListResponse(BaseModel):
    eventos: List[EventoResponse]
    total: int
    page: int
    size: int