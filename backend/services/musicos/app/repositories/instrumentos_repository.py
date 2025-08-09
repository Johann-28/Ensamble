from sqlite3 import IntegrityError
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.musicos import (
    InstrumentoCreate, InstrumentoUpdate, 
)


from .base_repository import BaseRepository
from app.models.catalogos import CatInstrumentos
import logging

logger = logging.getLogger(__name__)

class InstrumentosRepository(BaseRepository[CatInstrumentos]):
    def __init__(self, db: Session):
        super().__init__(db, CatInstrumentos)
    
    def get_by_codigo(self, codigo: str) -> Optional[CatInstrumentos]:
        """Obtener instrumento por código"""
        try:
            return self.db.query(CatInstrumentos).filter(
                CatInstrumentos.codigo == codigo,
                CatInstrumentos.activo == True
            ).first()
        except Exception as e:
            logger.error(f"Error obteniendo instrumento por código '{codigo}': {e}")
            raise
    
    def get_all_active(self) -> List[CatInstrumentos]:
        """Obtener todos los instrumentos activos ordenados"""
        try:
            return self.db.query(CatInstrumentos).filter(
                CatInstrumentos.activo == True
            ).order_by(CatInstrumentos.orden).all()
        except Exception as e:
            logger.error("Error obteniendo instrumentos activos")
            raise
    
    def get_by_familia(self, familia: str) -> List[CatInstrumentos]:
        """Obtener instrumentos por familia"""
        try:
            return self.db.query(CatInstrumentos).filter(
                CatInstrumentos.familia == familia,
                CatInstrumentos.activo == True
            ).order_by(CatInstrumentos.orden).all()
        except Exception as e:
            logger.error(f"Error obteniendo instrumentos de familia '{familia}': {e}")
            raise

    def create(self, instrumento_data: InstrumentoCreate) -> CatInstrumentos:
        """Crear un nuevo instrumento"""
        try:
            # Verificar que el código no exista
            existing = self.get_by_codigo(instrumento_data.codigo)
            if existing:
                raise ValueError(f"Ya existe un instrumento con el código '{instrumento_data.codigo}'")
            
            instrumento_dict = instrumento_data.model_dump()
            instrumento_dict['activo'] = True  # Por defecto activo
            
            return super().create(instrumento_dict)
        except IntegrityError as e:
            logger.error(f"Error de integridad creando instrumento: {e}")
            raise ValueError("Error de integridad: código duplicado o datos inválidos")
        except Exception as e:
            logger.error(f"Error creando instrumento: {e}")
            raise
    
    def update(self, instrumento_id: int, instrumento_data: InstrumentoUpdate) -> Optional[CatInstrumentos]:
        """Actualizar un instrumento existente"""
        try:
            # Verificar código único si se está actualizando
            if instrumento_data.codigo:
                existing = self.get_by_codigo(instrumento_data.codigo)
                if existing and existing.id != instrumento_id:
                    raise ValueError(f"Ya existe un instrumento con el código '{instrumento_data.codigo}'")
            
            update_data = instrumento_data.model_dump(exclude_unset=True)
            return super().update(instrumento_id, update_data)
        except Exception as e:
            logger.error(f"Error actualizando instrumento {instrumento_id}: {e}")
            raise
    
    def get_by_codigo(self, codigo: str) -> Optional[CatInstrumentos]:
        """Obtener instrumento por código"""
        try:
            return self.db.query(CatInstrumentos).filter(
                CatInstrumentos.codigo == codigo
            ).first()  # No filtrar por activo aquí para validaciones
        except Exception as e:
            logger.error(f"Error obteniendo instrumento por código '{codigo}': {e}")
            raise
    
    def get_all_active(self) -> List[CatInstrumentos]:
        """Obtener todos los instrumentos activos ordenados"""
        try:
            return self.db.query(CatInstrumentos).filter(
                CatInstrumentos.activo == True
            ).order_by(CatInstrumentos.orden).all()
        except Exception as e:
            logger.error("Error obteniendo instrumentos activos")
            raise
    
    def get_by_familia(self, familia: str) -> List[CatInstrumentos]:
        """Obtener instrumentos por familia"""
        try:
            return self.db.query(CatInstrumentos).filter(
                CatInstrumentos.familia == familia,
                CatInstrumentos.activo == True
            ).order_by(CatInstrumentos.orden).all()
        except Exception as e:
            logger.error(f"Error obteniendo instrumentos de familia '{familia}': {e}")
            raise
    
    def soft_delete(self, instrumento_id: int) -> bool:
        """Desactivar un instrumento (soft delete)"""
        try:
            instrumento = self.get_by_id(instrumento_id)
            if not instrumento:
                return False
            
            instrumento.activo = False
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error desactivando instrumento {instrumento_id}: {e}")
            self.db.rollback()
            raise
    
    def get_familias_disponibles(self) -> List[str]:
        """Obtener lista de familias de instrumentos activos"""
        try:
            from sqlalchemy import distinct
            result = (
                self.db.query(distinct(CatInstrumentos.familia))
                .filter(
                    CatInstrumentos.activo == True,
                    CatInstrumentos.familia.isnot(None)
                )
                .all()
            )
            return [familia[0] for familia in result if familia[0]]
        except Exception as e:
            logger.error(f"Error obteniendo familias de instrumentos: {e}")
            raise
    
    def get_all(self) -> List[CatInstrumentos]:
        """Obtener todos los instrumentos (activos e inactivos)"""
        try:
            return self.db.query(CatInstrumentos).order_by(CatInstrumentos.orden).all()
        except Exception as e:
            logger.error("Error obteniendo todos los instrumentos")
            raise