from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import Base
import logging

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Repository base con operaciones CRUD genéricas"""
    
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
    
    def get_by_id(self, id: Any) -> Optional[ModelType]:
        """Obtener por ID"""
        try:
            return self.db.query(self.model).filter(
                self.model.id == id
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"Error obteniendo {self.model.__name__} por ID {id}: {e}")
            raise
    
    def get_all(self, skip: int = 0, limit: int = 100, 
                filters: Optional[dict] = None) -> List[ModelType]:
        """Obtener todos con paginación y filtros opcionales"""
        try:
            query = self.db.query(self.model)
            
            # Aplicar filtros si existen
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        query = query.filter(getattr(self.model, field) == value)
            
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error obteniendo {self.model.__name__}: {e}")
            raise
    
    def count(self, filters: Optional[dict] = None) -> int:
        """Contar registros total"""
        try:
            query = self.db.query(self.model)
            
            # Aplicar filtros si existen
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        query = query.filter(getattr(self.model, field) == value)
            
            return query.count()
        except SQLAlchemyError as e:
            logger.error(f"Error contando {self.model.__name__}: {e}")
            raise
    
    def create(self, obj_data: dict) -> ModelType:
        """Crear nuevo registro"""
        try:
            db_obj = self.model(**obj_data)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Error creando {self.model.__name__}: {e}")
            self.db.rollback()
            raise
    
    def update(self, id: Any, obj_data: dict) -> Optional[ModelType]:
        """Actualizar registro existente"""
        try:
            db_obj = self.get_by_id(id)
            if not db_obj:
                return None
            
            # Actualizar solo campos que no sean None
            for field, value in obj_data.items():
                if value is not None and hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Error actualizando {self.model.__name__} {id}: {e}")
            self.db.rollback()
            raise
    
    def delete(self, id: Any) -> bool:
        """Eliminar registro (soft delete si tiene campo eliminado_en)"""
        try:
            db_obj = self.get_by_id(id)
            if not db_obj:
                return False
            
            # Soft delete si tiene el campo
            if hasattr(db_obj, 'eliminado_en'):
                from datetime import datetime
                db_obj.eliminado_en = datetime.utcnow()
            else:
                self.db.delete(db_obj)
            
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error eliminando {self.model.__name__} {id}: {e}")
            self.db.rollback()
            raise