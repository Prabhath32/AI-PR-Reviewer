from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import (
    Field,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="forbid",
        case_sensitive=False,
    )

    app_name: str = "AI PR Reviewer"
    app_env: Literal[
        "local", "test", "development",
        "staging", "production"
    ] = "local"

    app_version: str = "0.1.0"
    log_level: Literal[
        "DEBUG", "INFO", "WARNING",
        "ERROR", "CRITICAL"
    ] = "INFO"

    api_prefix: str = "/api/v1"
    cors_origins: list[str] = Field(default_factory=list)

    openai_api_key: SecretStr | None = None
    openai_model_name: str = "gpt-4.1-mini"

    database_url: SecretStr | None = None
    database_direct_url: SecretStr | None = None

    github_app_id: str | None = None
    github_app_private_key: SecretStr | None = None
    github_webhook_secret: SecretStr | None = None

    max_pr_files: int = Field(default=200, ge=1, le=3000)
    max_diff_bytes: int = Field(default=1_000_000, ge=1024)
    max_agent_steps: int = Field(default=12, ge=1, le=100)
    max_review_cost_usd: float = Field(default=1.0, gt=0)

    @field_validator(
        "openai_api_key",
        "database_url",
        "database_direct_url",
        "github_app_private_key",
        "github_webhook_secret",
        mode="before",
    )
    @classmethod
    def normalize_optional_secrets(
        cls, value: str | None
    ) -> str | None:
        return value or None

    @field_validator("github_app_id", mode="before")
    @classmethod
    def normalize_optional_id(
        cls, value: str | None
    ) -> str | None:
        return value or None

    @field_validator("api_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        if (
            not value.startswith("/")
            or value == "/"
            or value.endswith("/")
        ):
            raise ValueError(
                "API_PREFIX must start with '/' "
                "and not end with '/'"
            )
        return value

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.app_env == "production":
            if not self.database_url or not self.database_direct_url:
                raise ValueError("Production requires both database URLs")
            if not self.openai_api_key:
                raise ValueError("Production requires OPENAI_API_KEY")
            if "*" in self.cors_origins:
                raise ValueError("Wildcard CORS is disallowed in production")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
