from typing import List
from sqlalchemy.orm import Session

from app.models.catalogs import CatEstadosEvento


class EstadosEventoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[CatEstadosEvento]:
        """Obtener todos los estados de evento activos"""
        return self.db.query(CatEstadosEvento).filter(
            CatEstadosEvento.activo == True
        ).order_by(CatEstadosEvento.orden).all()
    
    def get_by_codigo(self, codigo: str) -> CatEstadosEvento:
        """Obtener estado de evento por código"""
        estado = self.db.query(CatEstadosEvento).filter(
            CatEstadosEvento.codigo == codigo
        ).first()
        if not estado:
            raise ValueError(f"Estado de evento no encontrado: {codigo}")
        return estado
    
    def get_by_id(self, estado_id: int) -> CatEstadosEvento:
        """Obtener estado de evento por ID"""
        estado = self.db.query(CatEstadosEvento).filter(
            CatEstadosEvento.id == estado_id
        ).first()
        if not estado:
            raise ValueError(f"Estado de evento no encontrado con ID: {estado_id}")
        return estado
    
    def get_estado_inicial(self) -> CatEstadosEvento:
        """Obtener estado inicial de planificación"""
        return self.get_by_codigo("planificacion")
