from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    """Centralised, immutable settings."""

    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    dynamodb_table: str = os.getenv("DYNAMODB_TABLE_NAME", "url_shortener")
    ec2_public_ip: str = os.getenv("EC2_PUBLIC_IP", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    cors_origins: list[str] = field(
        default_factory=lambda: [o.strip()
                                 for o in os.getenv("CORS_ORIGINS", "*").split(",")
                                 if o.strip()]
    )


settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    dynamo_table: str = "url-shortener-links"
    region: str = "eu-west-1"

    class Config:
        env_prefix = "URL_SHORTENER_"   # lee URL_SHORTENER_DYNAMO_TABLE del env

settings = Settings()
