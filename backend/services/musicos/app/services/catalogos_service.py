from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.core.transaction_manager import TransactionManager
from app.repositories.estados_musico_repository import EstadosMusicoRepository
from app.repositories.instrumentos_repository import InstrumentosRepository
from app.schemas.musicos import EstadoMusicoResponse, InstrumentoResponse

logger = logging.getLogger(__name__)

class CatalogosService:
    """Servicio especializado para gestión de catálogos"""
    
    def __init__(self, db: Session):
        self.db = db
        self.transaction_manager = TransactionManager(db)
        self.estados_repo = EstadosMusicoRepository(db)
        self.instrumentos_repo = InstrumentosRepository(db)
    
    def get_estados_musico(self, activos_solo: bool = True) -> List[EstadoMusicoResponse]:
        """Obtener catálogo de estados de músico"""
        with self.transaction_manager.read_only_transaction():
            if activos_solo:
                estados = self.estados_repo.get_all_active()
            else:
                estados = self.estados_repo.get_all()
            return [EstadoMusicoResponse.model_validate(estado) for estado in estados]
    
    def get_instrumentos_disponibles(self, activos_solo: bool = True) -> List[InstrumentoResponse]:
        """Obtener catálogo de instrumentos disponibles"""
        with self.transaction_manager.read_only_transaction():
            if activos_solo:
                instrumentos = self.instrumentos_repo.get_all_active()
            else:
                instrumentos = self.instrumentos_repo.get_all()
            return [InstrumentoResponse.model_validate(inst) for inst in instrumentos]
    
    def get_instrumentos_by_familia(self, familia: str) -> List[InstrumentoResponse]:
        """Obtener instrumentos por familia"""
        with self.transaction_manager.read_only_transaction():
            instrumentos = self.instrumentos_repo.get_by_familia(familia, activos_solo=True)
            return [InstrumentoResponse.model_validate(inst) for inst in instrumentos]
    
    def get_familias_instrumentos(self) -> List[str]:
        """Obtener lista de familias de instrumentos disponibles"""
        with self.transaction_manager.read_only_transaction():
            return self.instrumentos_repo.get_familias_disponibles()
