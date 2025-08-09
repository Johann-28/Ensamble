from fastapi import APIRouter
from .musicos import router as musicos_router
from .instrumentos import router as instrumentos_router

api_router = APIRouter()

api_router.include_router(
    musicos_router, 
    prefix="/musicos", 
    tags=["Músicos"]
)

api_router.include_router(
    instrumentos_router, 
    prefix="/musicos", 
    tags=["Instrumentos"]
)