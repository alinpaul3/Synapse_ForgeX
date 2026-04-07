import os
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "sqlite:///./synapse_forgex.db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # YouTube OAuth
    youtube_client_id: str = ""
    youtube_client_secret: str = ""
    youtube_redirect_uri: str = "http://localhost:8000/api/auth/youtube/callback"

    # Reddit OAuth
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_redirect_uri: str = "http://localhost:8000/api/auth/reddit/callback"
    reddit_user_agent: str = "SynapseForgeX/1.0"

    # ML Pipeline
    ml_pipeline_url: str = "http://localhost:8001/predict"

    # App
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    cors_origins: List[str] = ["chrome-extension://*", "http://localhost:3000", "http://localhost:5173"]

    # Encryption
    encryption_key: str = "default-encryption-key-change-me="


settings = Settings()
