from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    database_schema: str = "servicio_eventos"
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Eventos Service"
    debug: bool = False
    
    # Security
    secret_key: str
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()