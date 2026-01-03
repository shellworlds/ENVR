"""
API Configuration Settings
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "ENVR Quantum API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Quantum Computing REST API"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/quantum_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Quantum
    IBM_QUANTUM_TOKEN: Optional[str] = None
    QUANTUM_SIMULATOR: str = "qasm_simulator"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
