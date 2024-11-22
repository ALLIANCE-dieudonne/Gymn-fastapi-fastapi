from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache

class Settings(BaseSettings):
    #API config
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GymnREST"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    
   
    # Database settings
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "fils1?"
    DB_NAME: str = "gymn_management"
    DB_PORT: int = 3306
    DB_POOL_SIZE: int = 10
    DB_POOL_TIMEOUT: int = 30
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
  

@lru_cache
def get_settings() -> Settings:
    return Settings()
        
settings = Settings()

