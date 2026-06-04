import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "One Spirit Asia Operations System"
    API_V1_STR: str = "/api/v1"
    ENV: str = "development"  # development, staging, production
    AUTO_CREATE_TABLES: bool = True
    
    # Environment configs loaded by docker-compose or .env
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "onespirit_user"
    DB_PASSWORD: str = "onespirit_pass"
    DB_NAME: str = "onespirit_db"

    # Security
    JWT_SECRET: str = "supersecret_change_me_in_production_1234567890!"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://localhost:8001"
    ]

    # Uploads
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 10

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: any) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            import json
            if isinstance(v, str):
                try:
                    v = json.loads(v)
                except Exception:
                    pass
            if isinstance(v, list):
                return v
        return [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:8000",
            "http://localhost:8001"
        ]

    @model_validator(mode="after")
    def validate_jwt_secret_in_production(self) -> "Settings":
        if self.ENV == "production" and self.JWT_SECRET == "supersecret_change_me_in_production_1234567890!":
            raise ValueError(
                "SECURITY ERROR: JWT_SECRET must be changed from the default value in a production environment!"
            )
        return self

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

