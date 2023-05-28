import secrets
from pydantic import BaseSettings, AnyHttpUrl
from typing import List, Optional


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Study Assistant"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
    ]

    ADMIN_CODE = ["ADMIN", "TEACHER"]

    class Config:
        case_sensitive = True


settings = Settings()
