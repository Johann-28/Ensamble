from typing import List, Optional
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from app.models.catalogos import CatEstadosMusico
import logging

logger = logging.getLogger(__name__)

class EstadosMusicoRepository(BaseRepository[CatEstadosMusico]):
    def __init__(self, db: Session):
        super().__init__(db, CatEstadosMusico)
    
    def get_by_codigo(self, codigo: str) -> Optional[CatEstadosMusico]:
        """Obtener estado por código"""
        try:
            return self.db.query(CatEstadosMusico).filter(
                CatEstadosMusico.codigo == codigo,
                CatEstadosMusico.activo == True
            ).first()
        except Exception as e:
            logger.error(f"Error obteniendo estado por código '{codigo}': {e}")
            raise
    
    def get_all_active(self) -> List[CatEstadosMusico]:
        """Obtener todos los estados activos ordenados"""
        try:
            return self.db.query(CatEstadosMusico).filter(
                CatEstadosMusico.activo == True
            ).order_by(CatEstadosMusico.orden).all()
        except Exception as e:
            logger.error("Error obteniendo estados activos")
            raise