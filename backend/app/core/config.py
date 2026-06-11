import os
from typing import Any, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, model_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    PROJECT_NAME: str = "One Spirit Asia Operations System"
    API_V1_STR: str = "/api/v1"
    ENV: str = "development"  # development, staging, production
    DEBUG: bool = False
    AUTO_CREATE_TABLES: bool = True
    SEED_DEMO_USER: bool = True
    SEED_PLACEHOLDER_USERS: bool = True
    
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

    # Seed Admin Credentials
    ADMIN_EMAIL: str = "admin@onespirit.asia"
    ADMIN_PASSWORD: str = "OneSpirit2026!"

    # Seed Demo Credentials
    DEMO_EMAIL: str = "demo@onespirit.asia"
    DEMO_PASSWORD: str = "OneSpiritDemo2026!"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://localhost:8001",
        "https://osgueh-dotcom.github.io"
    ]

    # Uploads
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 10

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug_flag(cls, value: Any) -> Any:
        if not isinstance(value, str):
            return value

        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on", "debug", "development"}:
            return True
        if normalized in {"0", "false", "no", "off", "release", "production"}:
            return False
        return value

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
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
            "http://localhost:8001",
            "https://osgueh-dotcom.github.io"
        ]

    @model_validator(mode="after")
    def validate_security_in_production(self) -> "Settings":
        if self.ENV == "production":
            if self.DEBUG:
                raise ValueError(
                    "SECURITY ERROR: DEBUG must be disabled in a production environment!"
                )
            if self.DB_PASSWORD == "onespirit_pass":
                raise ValueError(
                    "SECURITY ERROR: DB_PASSWORD must be changed from the default value in a production environment!"
                )
            if self.SEED_DEMO_USER:
                raise ValueError(
                    "SECURITY ERROR: SEED_DEMO_USER must be disabled in a production environment!"
                )
            if self.SEED_PLACEHOLDER_USERS:
                raise ValueError(
                    "SECURITY ERROR: SEED_PLACEHOLDER_USERS must be disabled in a production environment!"
                )
            if self.JWT_SECRET == "supersecret_change_me_in_production_1234567890!":
                raise ValueError(
                    "SECURITY ERROR: JWT_SECRET must be changed from the default value in a production environment!"
                )
            if self.ADMIN_PASSWORD == "OneSpirit2026!":
                raise ValueError(
                    "SECURITY ERROR: ADMIN_PASSWORD must be changed from the default value in a production environment!"
                )
            if self.DEMO_PASSWORD == "OneSpiritDemo2026!":
                raise ValueError(
                    "SECURITY ERROR: DEMO_PASSWORD must be changed from the default value in a production environment!"
                )
        return self

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()

