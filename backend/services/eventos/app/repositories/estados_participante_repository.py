from typing import List
from sqlalchemy.orm import Session

from app.models.catalogs import CatEstadosParticipante


class EstadosParticipanteRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[CatEstadosParticipante]:
        """Obtener catálogo de estados de participante"""
        return self.db.query(CatEstadosParticipante).filter(
            CatEstadosParticipante.activo == True
        ).order_by(CatEstadosParticipante.orden).all()
    
    def get_by_codigo(self, codigo: str) -> CatEstadosParticipante:
        """Obtener estado de participante por código"""
        estado = self.db.query(CatEstadosParticipante).filter(
            CatEstadosParticipante.codigo == codigo
        ).first()
        if not estado:
            raise ValueError(f"Estado de participante no encontrado: {codigo}")
        return estado
    
    def get_by_id(self, estado_id: int) -> CatEstadosParticipante:
        """Obtener estado de participante por ID"""
        estado = self.db.query(CatEstadosParticipante).filter(
            CatEstadosParticipante.id == estado_id
        ).first()
        if not estado:
            raise ValueError(f"Estado de participante no encontrado con ID: {estado_id}")
        return estado
