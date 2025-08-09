from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class TransactionManager:
    """Manejo centralizado de transacciones para servicios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    @contextmanager
    def transaction(self):
        """Context manager para manejo de transacciones con rollback automático"""
        try:
            logger.debug("Iniciando transacción")
            yield self.db
            self.db.commit()
            logger.debug("Transacción completada exitosamente")
        except SQLAlchemyError as e:
            logger.error(f"Error de SQLAlchemy, haciendo rollback: {e}")
            self.db.rollback()
            raise
        except Exception as e:
            logger.error(f"Error inesperado, haciendo rollback: {e}")
            self.db.rollback()
            raise
    
    @contextmanager
    def read_only_transaction(self):
        """Context manager para transacciones de solo lectura"""
        try:
            logger.debug("Iniciando transacción de solo lectura")
            yield self.db
            # No hacer commit en transacciones de solo lectura
            logger.debug("Transacción de solo lectura completada")
        except Exception as e:
            logger.error(f"Error en transacción de solo lectura: {e}")
            # No es necesario rollback para operaciones de solo lectura
            raise
    
    def execute_in_transaction(self, operation_func, *args, **kwargs):
        """Ejecutar una función dentro de una transacción"""
        with self.transaction():
            return operation_func(*args, **kwargs)
