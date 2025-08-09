from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

# Esquemas para catálogos
class EstadoMusicoResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True
    orden: int = 1
    model_config = ConfigDict(from_attributes=True)


class InstrumentoResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    familia: Optional[str] = None
    descripcion: Optional[str] = None
    activo: bool = True
    orden: int = 1
    model_config = ConfigDict(from_attributes=True)


class NivelHabilidadResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True
    orden: int = 1
    model_config = ConfigDict(from_attributes=True)

#Instrumentos

class InstrumentoCreate(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50, description="Código único del instrumento")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del instrumento")
    familia: Optional[str] = Field(None, max_length=50, description="Familia del instrumento (cuerda, viento, etc.)")
    descripcion: Optional[str] = Field(None, description="Descripción del instrumento")
    orden: int = Field(1, ge=1, description="Orden para mostrar en listas")

class InstrumentoUpdate(BaseModel):
    codigo: Optional[str] = Field(None, min_length=1, max_length=50)
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    familia: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
    orden: Optional[int] = Field(None, ge=1)


# Esquemas para instrumentos del músico
class InstrumentoMusicoBase(BaseModel):
    instrumento_id: int
    nivel_id: int
    es_principal: bool = False
    fecha_inicio: Optional[date] = None
    notas: Optional[str] = None

class InstrumentoMusicoCreate(InstrumentoMusicoBase):
    pass

class InstrumentoMusicoUpdate(BaseModel):
    instrumento_id: Optional[int] = None
    nivel_id: Optional[int] = None
    es_principal: Optional[bool] = None
    fecha_inicio: Optional[date] = None
    notas: Optional[str] = None


class InstrumentoMusicoResponse(InstrumentoMusicoBase):
    id: UUID
    musico_id: UUID
    instrumento: Optional[InstrumentoResponse] = None
    nivel: Optional[NivelHabilidadResponse] = None
    model_config = ConfigDict(from_attributes=True)

# Esquemas para músicos
class MusicoBase(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=1, max_length=255)
    telefono: Optional[str] = Field(None, max_length=50)
    url_foto_perfil: Optional[str] = None

class MusicoCreate(MusicoBase):
    estado_codigo: str = "activo"
    fecha_ingreso: Optional[datetime] = None

class MusicoUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    telefono: Optional[str] = Field(None, max_length=50)
    estado_codigo: Optional[str] = None
    url_foto_perfil: Optional[str] = None


class MusicoResponse(MusicoBase):
    id: UUID
    fecha_ingreso: datetime
    estado: EstadoMusicoResponse
    instrumentos: List[InstrumentoMusicoResponse] = []
    creado_en: datetime
    actualizado_en: Optional[datetime] = None
    eliminado_en: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# Respuestas con paginación
class MusicosListResponse(BaseModel):
    musicos: List[MusicoResponse]
    total: int
    page: int
    size: int

