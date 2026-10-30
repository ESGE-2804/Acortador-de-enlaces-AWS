"""Application configuration loaded from environment variables."""

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
