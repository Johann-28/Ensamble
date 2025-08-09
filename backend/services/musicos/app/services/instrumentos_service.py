from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.core.transaction_manager import TransactionManager
from app.core.validation_service import ValidationService
from app.repositories.instrumentos_musico_repository import InstrumentosMusicoRepository
from app.repositories.instrumentos_repository import InstrumentosRepository
from app.schemas.musicos import (
    InstrumentoMusicoCreate, InstrumentoMusicoUpdate, InstrumentoMusicoResponse
)

logger = logging.getLogger(__name__)

class InstrumentosService:
    """Servicio especializado para gestión de instrumentos de músicos"""
    
    def __init__(self, db: Session):
        self.db = db
        self.transaction_manager = TransactionManager(db)
        self.validation_service = ValidationService(db)
        self.instrumentos_repo = InstrumentosMusicoRepository(db)
        self.catalogo_repo = InstrumentosRepository(db)
    
    def assign_instrumento_to_musico(
        self, 
        musico_id: UUID, 
        instrumento_data: InstrumentoMusicoCreate
    ) -> InstrumentoMusicoResponse:
        """Asignar un instrumento a un músico con validaciones"""
        
        # Validaciones de negocio
        self.validation_service.validate_instrumento_assignment(
            musico_id=musico_id,
            instrumento_id=instrumento_data.instrumento_id,
            is_principal=instrumento_data.es_principal,
            instrumentos_repo=self.instrumentos_repo,
            catalogo_repo=self.catalogo_repo
        )
        
        # Transacción segura
        with self.transaction_manager.transaction():
            db_instrumento = self.instrumentos_repo.create(instrumento_data, musico_id)
            return InstrumentoMusicoResponse.model_validate(db_instrumento)
    
    def remove_instrumento_from_musico(
        self, 
        musico_id: UUID, 
        instrumento_id: int
    ) -> dict:
        """Eliminar instrumento de un músico"""
        
        # Validaciones de negocio
        self.validation_service.validate_instrumento_removal(
            musico_id, instrumento_id, self.instrumentos_repo
        )
        
        # Transacción segura
        with self.transaction_manager.transaction():
            success = self.instrumentos_repo.delete_by_musico_and_instrumento(musico_id, instrumento_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Instrumento no encontrado para este músico"
                )
            return {"message": "Instrumento eliminado correctamente"}
    
    def get_instrumentos_by_musico(self, musico_id: UUID) -> List[InstrumentoMusicoResponse]:
        """Obtener todos los instrumentos de un músico"""
        with self.transaction_manager.read_only_transaction():
            instrumentos = self.instrumentos_repo.get_by_musico(musico_id)
            return [InstrumentoMusicoResponse.model_validate(inst) for inst in instrumentos]
    
    def update_instrumento(
        self, 
        instrumento_id: UUID, 
        instrumento_data: InstrumentoMusicoUpdate
    ) -> InstrumentoMusicoResponse:
        """Actualizar un instrumento de músico"""
        
        with self.transaction_manager.transaction():
            db_instrumento = self.instrumentos_repo.update(instrumento_id, instrumento_data)
            if not db_instrumento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Instrumento no encontrado"
                )
            return InstrumentoMusicoResponse.model_validate(db_instrumento)
