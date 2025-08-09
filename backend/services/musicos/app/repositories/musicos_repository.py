from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from uuid import UUID

from .base_repository import BaseRepository
from app.models.musicos import Musico
from app.schemas.musicos import MusicoCreate, MusicoUpdate
import logging

logger = logging.getLogger(__name__)

class MusicosRepository(BaseRepository[Musico]):
    def __init__(self, db: Session):
        super().__init__(db, Musico)
    
    def create(self, musico_data: MusicoCreate) -> Musico:
        """Crear un nuevo músico"""
        try:
            # Obtener estado por código
            from .estados_musico_repository import EstadosMusicoRepository
            estados_repo = EstadosMusicoRepository(self.db)
            estado = estados_repo.get_by_codigo(musico_data.estado_codigo)
            
            if not estado:
                raise ValueError(f"Estado '{musico_data.estado_codigo}' no encontrado")
            
            musico_dict = musico_data.model_dump(exclude={'estado_codigo'})
            musico_dict['estado_id'] = estado.id
            
            return super().create(musico_dict)
        except Exception as e:
            logger.error(f"Error creando músico: {e}")
            raise
    
    def update(self, musico_id: UUID, musico_data: MusicoUpdate) -> Optional[Musico]:
        """Actualizar un músico existente"""
        try:
            update_data = {}
            
            # Manejar actualización de estado si se proporciona
            if musico_data.estado_codigo:
                from .estados_musico_repository import EstadosMusicoRepository
                estados_repo = EstadosMusicoRepository(self.db)
                estado = estados_repo.get_by_codigo(musico_data.estado_codigo)
                
                if not estado:
                    raise ValueError(f"Estado '{musico_data.estado_codigo}' no encontrado")
                
                update_data['estado_id'] = estado.id
            
            # Agregar otros campos para actualizar
            for field, value in musico_data.model_dump(exclude={'estado_codigo'}, exclude_unset=True).items():
                if value is not None:
                    update_data[field] = value
            
            return super().update(musico_id, update_data)
        except Exception as e:
            logger.error(f"Error actualizando músico {musico_id}: {e}")
            raise
    
    def get_all_with_relationships(self, skip: int = 0, limit: int = 100, 
                                 activos_solo: bool = True) -> List[Musico]:
        """Obtener músicos con sus relaciones cargadas"""
        try:
            query = self.db.query(Musico).options(
                joinedload(Musico.estado),
                joinedload(Musico.instrumentos)
            )
            
            # Filtrar solo activos si se solicita
            if activos_solo:
                query = query.filter(Musico.eliminado_en.is_(None))
            
            return query.offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error obteniendo músicos con relaciones: {e}")
            raise
    
    def get_by_id_with_relationships(self, musico_id: UUID) -> Optional[Musico]:
        """Obtener músico por ID con relaciones"""
        try:
            return self.db.query(Musico).options(
                joinedload(Musico.estado),
                joinedload(Musico.instrumentos)
            ).filter(
                and_(
                    Musico.id == musico_id,
                    Musico.eliminado_en.is_(None)
                )
            ).first()
        except Exception as e:
            logger.error(f"Error obteniendo músico {musico_id} con relaciones: {e}")
            raise
    
    def get_by_email(self, email: str) -> Optional[Musico]:
        """Obtener músico por email"""
        try:
            return self.db.query(Musico).filter(
                and_(
                    Musico.email == email,
                    Musico.eliminado_en.is_(None)
                )
            ).first()
        except Exception as e:
            logger.error(f"Error obteniendo músico por email {email}: {e}")
            raise
    
    def search_by_name(self, nombre: str, skip: int = 0, limit: int = 100) -> List[Musico]:
        """Buscar músicos por nombre"""
        try:
            return self.db.query(Musico).options(
                joinedload(Musico.estado),
                joinedload(Musico.instrumentos)
            ).filter(
                and_(
                    Musico.nombre.ilike(f'%{nombre}%'),
                    Musico.eliminado_en.is_(None)
                )
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error buscando músicos por nombre '{nombre}': {e}")
            raise