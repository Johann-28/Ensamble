from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class ValidationService:
    """Servicio centralizado para validaciones de reglas de negocio"""
    
    # Constantes de negocio
    MAX_INSTRUMENTOS_PRINCIPALES = 2
    MAX_INSTRUMENTOS_TOTAL = 5
    MIN_EDAD_MUSICO = 16
    MAX_LONGITUD_NOMBRE = 100
    DOMINIOS_EMAIL_PERMITIDOS = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com"]
    
    def __init__(self, db):
        self.db = db
    
    def validate_musico_creation(self, email: str, musicos_repo) -> None:
        """Validar creación de músico"""
        # Validar email único
        if musicos_repo.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado por otro músico"
            )
        
        # Validar dominio de email
        domain = email.split('@')[-1].lower() if '@' in email else ""
        if domain not in self.DOMINIOS_EMAIL_PERMITIDOS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dominio de email no permitido. Dominios válidos: {', '.join(self.DOMINIOS_EMAIL_PERMITIDOS)}"
            )
    
    def validate_musico_update(self, musico_id: UUID, email: str, musicos_repo) -> None:
        """Validar actualización de músico"""
        if email:
            existing = musicos_repo.get_by_email(email)
            if existing and existing.id != musico_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El email ya está registrado por otro músico"
                )
    
    def validate_instrumento_assignment(
        self, 
        musico_id: UUID, 
        instrumento_id: int, 
        is_principal: bool,
        instrumentos_repo,
        catalogo_repo
    ) -> None:
        """Validar asignación de instrumento a músico"""
        
        # Validar que el instrumento existe y está activo
        instrumento = catalogo_repo.get_by_id(instrumento_id)
        if not instrumento or not instrumento.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El instrumento no existe o no está disponible"
            )
        
        # Validar que el músico no tenga ya este instrumento
        existing = instrumentos_repo.get_by_musico_and_instrumento(musico_id, instrumento_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El músico ya tiene registrado este instrumento"
            )
        
        # Validar límites de instrumentos
        current_count = instrumentos_repo.count_by_musico(musico_id)
        if current_count >= self.MAX_INSTRUMENTOS_TOTAL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El músico no puede tener más de {self.MAX_INSTRUMENTOS_TOTAL} instrumentos"
            )
        
        # Validar límites de instrumentos principales
        if is_principal:
            principales_count = instrumentos_repo.count_principales_by_musico(musico_id)
            if principales_count >= self.MAX_INSTRUMENTOS_PRINCIPALES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El músico no puede tener más de {self.MAX_INSTRUMENTOS_PRINCIPALES} instrumentos principales"
                )
    
    def validate_instrumento_removal(
        self, 
        musico_id: UUID, 
        instrumento_id: int,
        instrumentos_repo
    ) -> None:
        """Validar eliminación de instrumento"""
        instrumento_musico = instrumentos_repo.get_by_musico_and_instrumento(musico_id, instrumento_id)
        if not instrumento_musico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El músico no tiene registrado este instrumento"
            )
    
    def validate_estado_change(self, estado_id: int, estados_repo) -> None:
        """Validar cambio de estado"""
        estado = estados_repo.get_by_id(estado_id)
        if not estado or not estado.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estado especificado no existe o no está disponible"
            )
    
    def validate_batch_operation(self, entity_ids: List[UUID]) -> None:
        """Validar operaciones en lote"""
        if not entity_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe especificar al menos un elemento para la operación"
            )
        
        if len(entity_ids) > 50:  # Límite de seguridad para operaciones batch
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pueden procesar más de 50 elementos a la vez"
            )
