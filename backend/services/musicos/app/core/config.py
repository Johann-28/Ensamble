from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    # Database
    database_url: str
    database_schema: str = "servicio_musicos"
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Musicos Service - Band Management System"
    debug: bool = False
    
    # Security
    secret_key: str = "change-this-secret-key-in-production"
    access_token_expire_minutes: int = 30
    
    # Para desarrollo
    def get_database_url(self) -> str:
        return self.database_url

settings = Settings()