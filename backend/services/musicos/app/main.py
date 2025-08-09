from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from app.core.config import settings
from app.api.v1 import api_router
from app.core.database import engine

# Configurar logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Iniciando {settings.project_name}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Verificar conexión a base de datos
    try:
        # Las tablas deben crearse manualmente con el script SQL
        # Esta línea solo verifica la conexión
        with engine.connect() as connection:
            logger.info("Conexión a base de datos exitosa")
    except Exception as e:
        logger.error(f"Error conectando a base de datos: {e}")
        raise
    yield
    logger.info("Cerrando aplicación")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    debug=settings.debug,
    docs_url="/swagger",  
    redoc_url="/redoc",   
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router, prefix=settings.api_v1_str)

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no manejado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Musicos-service",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,  # Puerto diferente para el servicio de músicos
        reload=settings.debug
    )
