from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID
from app.models.catalogos import CatInstrumentos

from .base_repository import BaseRepository
from app.models.musicos import InstrumentoMusico
from app.schemas.musicos import InstrumentoMusicoCreate, InstrumentoMusicoUpdate
import logging

logger = logging.getLogger(__name__)

class InstrumentosMusicoRepository(BaseRepository[InstrumentoMusico]):
    def __init__(self, db: Session):
        super().__init__(db, InstrumentoMusico)
    
    def create(self, instrumento_data: InstrumentoMusicoCreate, musico_id: UUID) -> InstrumentoMusico:
        """Crear un nuevo instrumento para un músico"""
        try:
            instrumento_dict = instrumento_data.model_dump()
            instrumento_dict['musico_id'] = musico_id
            
            return super().create(instrumento_dict)
        except Exception as e:
            logger.error(f"Error creando instrumento para músico {musico_id}: {e}")
            raise
    
    def count_by_musico(self, musico_id: UUID) -> int:
        """Contar instrumentos de un músico"""
        try:
            return self.db.query(InstrumentoMusico).filter(
                InstrumentoMusico.musico_id == musico_id
            ).count()
        except Exception as e:
            logger.error(f"Error contando instrumentos del músico {musico_id}: {e}")
            raise
    
    def count_principales_by_musico(self, musico_id: UUID) -> int:
        """Contar instrumentos principales de un músico"""
        try:
            return self.db.query(InstrumentoMusico).filter(
                and_(
                    InstrumentoMusico.musico_id == musico_id,
                    InstrumentoMusico.es_principal == True
                )
            ).count()
        except Exception as e:
            logger.error(f"Error contando instrumentos principales del músico {musico_id}: {e}")
            raise
    
    def get_by_musico_and_instrumento(self, musico_id: UUID, instrumento_id: int) -> Optional[InstrumentoMusico]:
        """Obtener instrumento específico de un músico"""
        try:
            return self.db.query(InstrumentoMusico).filter(
                and_(
                    InstrumentoMusico.musico_id == musico_id,
                    InstrumentoMusico.instrumento_id == instrumento_id
                )
            ).first()
        except Exception as e:
            logger.error(f"Error obteniendo instrumento {instrumento_id} del músico {musico_id}: {e}")
            raise
    
    def get_by_musico(self, musico_id: UUID) -> List[InstrumentoMusico]:
        """Obtener todos los instrumentos de un músico"""
        try:
            return self.db.query(InstrumentoMusico).filter(
                InstrumentoMusico.musico_id == musico_id
            ).all()
        except Exception as e:
            logger.error(f"Error obteniendo instrumentos del músico {musico_id}: {e}")
            raise
    
    def get_by_musico_and_instrumento(self, musico_id: UUID, instrumento_id: int) -> Optional[InstrumentoMusico]:
        """Verificar si un músico ya tiene registrado un instrumento"""
        try:
            return self.db.query(InstrumentoMusico).filter(
                and_(
                    InstrumentoMusico.musico_id == musico_id,
                    InstrumentoMusico.instrumento_id == instrumento_id
                )
            ).first()
        except Exception as e:
            logger.error(f"Error verificando instrumento {instrumento_id} del músico {musico_id}: {e}")
            raise
    
    def update(self, instrumento_id: UUID, instrumento_data: InstrumentoMusicoUpdate) -> Optional[InstrumentoMusico]:
        """Actualizar un instrumento de músico"""
        try:
            update_data = instrumento_data.model_dump(exclude_unset=True)
            return super().update(instrumento_id, update_data)
        except Exception as e:
            logger.error(f"Error actualizando instrumento {instrumento_id}: {e}")
            raise
    
    def delete_by_musico_and_instrumento(self, musico_id: UUID, instrumento_id: int) -> bool:
        """Eliminar un instrumento específico de un músico"""
        try:
            instrumento = self.get_by_musico_and_instrumento(musico_id, instrumento_id)
            if instrumento:
                self.db.delete(instrumento)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error eliminando instrumento {instrumento_id} del músico {musico_id}: {e}")
            self.db.rollback()
            raise

    def get_by_musico_with_details(self, musico_id: UUID) -> List[InstrumentoMusico]:
        """Obtener todos los instrumentos de un músico con detalles del catálogo"""
        try:
            
            return self.db.query(InstrumentoMusico).join(
                CatInstrumentos, InstrumentoMusico.instrumento_id == CatInstrumentos.id
            ).join(
                CatNivelesHabilidad, InstrumentoMusico.nivel_id == CatNivelesHabilidad.id
            ).filter(
                InstrumentoMusico.musico_id == musico_id
            ).all()
        except Exception as e:
            logger.error(f"Error obteniendo instrumentos del músico {musico_id} con detalles: {e}")
            raise