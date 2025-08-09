from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.instrumentos_repository import InstrumentosRepository
from app.schemas.musicos import InstrumentoCreate, InstrumentoResponse, InstrumentoUpdate, NivelHabilidadResponse
from fastapi import HTTPException, status

# Importar nuevos componentes arquitectónicos
from app.core.transaction_manager import TransactionManager
from app.core.validation_service import ValidationService
from app.services.instrumentos_service import InstrumentosService
from app.services.catalogos_service import CatalogosService

from app.repositories.musicos_repository import MusicosRepository
from app.repositories.estados_musico_repository import EstadosMusicoRepository
from app.repositories.instrumentos_musico_repository import InstrumentosMusicoRepository
from app.schemas.musicos import (
    MusicoCreate, MusicoUpdate, MusicoResponse,
    InstrumentoMusicoCreate, InstrumentoMusicoUpdate, InstrumentoMusicoResponse,
    EstadoMusicoResponse
)

from app.models.musicos import InstrumentoMusico, Musico, InstrumentoMusico
import logging

logger = logging.getLogger(__name__)

class MusicosService:
    def __init__(self, db: Session):
        self.db = db
        
        # Componentes arquitectónicos centrales
        self.transaction_manager = TransactionManager(db)
        self.validation_service = ValidationService(db)
        
        # Servicios especializados
        self.instrumentos_service = InstrumentosService(db)
        self.catalogos_service = CatalogosService(db)
        
        # Repositorios especializados
        self.musicos_repo = MusicosRepository(db)
        self.estados_repo = EstadosMusicoRepository(db)
        self.instrumentos_repo = InstrumentosMusicoRepository(db)
        self.catalogo_instrumentos_repo = InstrumentosRepository(db)

    
    def create_musico(self, musico_data: MusicoCreate) -> MusicoResponse:
        """Crear un nuevo músico con validaciones y transacciones seguras"""
        try:
            # Validaciones de negocio centralizadas
            self.validation_service.validate_musico_creation(
                musico_data.email, self.musicos_repo
            )
            
            # Transacción segura con rollback automático
            with self.transaction_manager.transaction():
                db_musico = self.musicos_repo.create(musico_data)
                return self._musico_to_response(db_musico)
                
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error creando músico: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    def get_musico(self, musico_id: UUID) -> MusicoResponse:
        """Obtener un músico por ID"""
        db_musico = self.musicos_repo.get_by_id_with_relationships(musico_id)
        if not db_musico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Músico no encontrado"
            )
        return self._musico_to_response(db_musico)
    
    def get_musicos(self, skip: int = 0, limit: int = 100, activos_solo: bool = True) -> Tuple[List[MusicoResponse], int]:
        """Obtener lista de músicos con paginación"""
        if limit > 100:
            limit = 100
        
        musicos = self.musicos_repo.get_all_with_relationships(skip=skip, limit=limit, activos_solo=activos_solo)
        total = self.musicos_repo.count(filters={'eliminado_en': None} if activos_solo else None)
        
        musicos_response = [self._musico_to_response(musico) for musico in musicos]
        return musicos_response, total
    
    def update_musico(self, musico_id: UUID, musico_data: MusicoUpdate) -> MusicoResponse:
        """Actualizar un músico con validaciones y transacciones seguras"""
        try:
            # Validaciones de negocio centralizadas
            if musico_data.email:
                self.validation_service.validate_musico_update(
                    musico_id, musico_data.email, self.musicos_repo
                )
            
            # Transacción segura con rollback automático
            with self.transaction_manager.transaction():
                db_musico = self.musicos_repo.update(musico_id, musico_data)
                if not db_musico:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Músico no encontrado"
                    )
                
                # Recargar con relaciones
                db_musico = self.musicos_repo.get_by_id_with_relationships(musico_id)
                return self._musico_to_response(db_musico)
                
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def delete_musico(self, musico_id: UUID) -> dict:
        """Eliminar un músico (soft delete)"""
        if not self.musicos_repo.delete(musico_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Músico no encontrado"
            )
        return {"message": "Músico eliminado correctamente"}
    
    def search_musicos(self, nombre: str, skip: int = 0, limit: int = 100) -> List[MusicoResponse]:
        """Buscar músicos por nombre"""
        if limit > 100:
            limit = 100
        
        musicos = self.musicos_repo.search_by_name(nombre, skip=skip, limit=limit)
        return [self._musico_to_response(musico) for musico in musicos]
    
    # ==================== MÉTODOS PARA INSTRUMENTOS ====================
    
    def add_instrumento(self, musico_id: UUID, instrumento_data: InstrumentoMusicoCreate) -> InstrumentoMusicoResponse:
        """Agregar un instrumento a un músico - Delegando al servicio especializado"""
        # Verificar que el músico existe
        musico = self.musicos_repo.get_by_id(musico_id)
        if not musico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Músico no encontrado"
            )
        
        # Delegar al servicio especializado de instrumentos
        return self.instrumentos_service.assign_instrumento_to_musico(musico_id, instrumento_data)
    
    def get_instrumentos_musico(self, musico_id: UUID) -> List[InstrumentoMusicoResponse]:
        """Obtener todos los instrumentos de un músico - Delegando al servicio especializado"""
        # Verificar que el músico existe
        musico = self.musicos_repo.get_by_id(musico_id)
        if not musico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Músico no encontrado"
            )
        
        # Delegar al servicio especializado
        return self.instrumentos_service.get_instrumentos_by_musico(musico_id)
    
    def remove_instrumento(self, musico_id: UUID, instrumento_id: int) -> dict:
        """Eliminar un instrumento de un músico - Delegando al servicio especializado"""
        return self.instrumentos_service.remove_instrumento_from_musico(musico_id, instrumento_id)
    
    def get_instrumentos_disponibles(self) -> List[InstrumentoResponse]:
        """Obtener catálogo de instrumentos disponibles - Delegando al servicio de catálogos"""
        return self.catalogos_service.get_instrumentos_disponibles()
    
    def get_instrumentos_by_familia(self, familia: str) -> List[InstrumentoResponse]:
        """Obtener instrumentos por familia - Delegando al servicio de catálogos"""
        return self.catalogos_service.get_instrumentos_by_familia(familia)
    
    # ==================== MÉTODOS PARA CATÁLOGOS ====================
    
    def get_estados_musico(self) -> List[EstadoMusicoResponse]:
        """Obtener catálogo de estados de músico - Delegando al servicio de catálogos"""
        return self.catalogos_service.get_estados_musico()
    
    # ==================== MÉTODOS PRIVADOS ====================
    
    def _musico_to_response(self, musico: Musico) -> MusicoResponse:
        """Convertir modelo de músico a response schema"""
        instrumentos = [self._instrumento_to_response(inst) for inst in musico.instrumentos] if musico.instrumentos else []
        
        return MusicoResponse(
            id=musico.id,
            email=musico.email,
            nombre=musico.nombre,
            telefono=musico.telefono,
            fecha_ingreso=musico.fecha_ingreso,
            estado=EstadoMusicoResponse.model_validate(musico.estado),
            instrumentos=instrumentos,
            url_foto_perfil=musico.url_foto_perfil,
            creado_en=musico.creado_en,
            actualizado_en=musico.actualizado_en,
            eliminado_en=musico.eliminado_en
        )
    
    def _instrumento_to_response(self, instrumento: InstrumentoMusico) -> InstrumentoMusicoResponse:
        """Convertir modelo de instrumento a response schema"""
        return InstrumentoMusicoResponse.model_validate(instrumento)
    
    def _instrumento_to_response_with_details(self, instrumento: InstrumentoMusico) -> InstrumentoMusicoResponse:
        # Obtener detalles del instrumento y nivel
        instrumento_detalle = self.catalogo_instrumentos_repo.get_by_id(instrumento.instrumento_id)
        
        response_data = InstrumentoMusicoResponse.model_validate(instrumento)
        
        if instrumento_detalle:
            response_data.instrumento = InstrumentoResponse.model_validate(instrumento_detalle)
       
            
        return response_data

    #Instrumentos
    
    def create_instrumento(self, instrumento_data: InstrumentoCreate) -> InstrumentoResponse:
        """Crear un nuevo instrumento en el catálogo"""
        try:
            db_instrumento = self.catalogo_instrumentos_repo.create(instrumento_data)
            return InstrumentoResponse.model_validate(db_instrumento)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error creando instrumento: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

    def update_instrumento(self, instrumento_id: int, instrumento_data: InstrumentoUpdate) -> InstrumentoResponse:
        """Actualizar un instrumento del catálogo"""
        try:
            db_instrumento = self.catalogo_instrumentos_repo.update(instrumento_id, instrumento_data)
            if not db_instrumento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Instrumento no encontrado"
                )
            return InstrumentoResponse.model_validate(db_instrumento)
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error actualizando instrumento {instrumento_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

    def delete_instrumento(self, instrumento_id: int) -> dict:
        """Desactivar un instrumento (soft delete)"""
        if not self.catalogo_instrumentos_repo.soft_delete(instrumento_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Instrumento no encontrado"
            )
        return {"message": "Instrumento desactivado correctamente"}