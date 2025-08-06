from fastapi import APIRouter
from .eventos import router as Eventos_router

api_router = APIRouter()

api_router.include_router(
    Eventos_router, 
    prefix="/eventos", 
    tags=["Eventos"]
)