from typing import List
from sqlalchemy.orm import Session

from app.models.catalogs import CatTiposEvento


class TiposEventoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[CatTiposEvento]:
        """Obtener todos los tipos de evento activos"""
        return self.db.query(CatTiposEvento).filter(
            CatTiposEvento.activo == True
        ).order_by(CatTiposEvento.orden).all()
    
    def get_by_codigo(self, codigo: str) -> CatTiposEvento:
        """Obtener tipo de evento por código"""
        tipo = self.db.query(CatTiposEvento).filter(
            CatTiposEvento.codigo == codigo
        ).first()
        if not tipo:
            raise ValueError(f"Tipo de evento no encontrado: {codigo}")
        return tipo
    
    def get_by_id(self, tipo_id: int) -> CatTiposEvento:
        """Obtener tipo de evento por ID"""
        tipo = self.db.query(CatTiposEvento).filter(
            CatTiposEvento.id == tipo_id
        ).first()
        if not tipo:
            raise ValueError(f"Tipo de evento no encontrado con ID: {tipo_id}")
        return tipo
