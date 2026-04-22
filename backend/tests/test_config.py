import pytest
from app.config import settings


def test_settings_have_defaults():
    """Test that settings have default values."""
    assert settings.jwt_algorithm == "HS256"
    assert settings.jwt_expire_minutes > 0
    assert settings.app_port == 8000
    assert isinstance(settings.cors_origins, list)


def test_database_url_set():
    """Test that database URL is configured."""
    assert settings.database_url is not None
    assert len(settings.database_url) > 0
