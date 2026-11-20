
import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_defaults_without_env_file():
    settings = Settings(_env_file=None, app_env="test")

    assert settings.api_prefix == "/api/v1"
    assert settings.openai_api_key is None


def test_secret_is_not_displayed():
    settings = Settings(
        _env_file=None,
        app_env="test",
        openai_api_key="secret-for-test",
    )

    assert "secret-for-test" not in repr(settings)


def test_production_rejects_missing_credentials():
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            app_env="production",
            database_url="",
            openai_api_key="",
        )
