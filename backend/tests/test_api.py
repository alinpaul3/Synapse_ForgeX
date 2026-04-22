import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_auth_start_no_db():
    """Test that /api/auth/start handles DB errors gracefully."""
    with patch("app.api.auth.get_db") as mock_db:
        mock_session = MagicMock()
        mock_session.__enter__ = lambda s: s
        mock_session.__exit__ = MagicMock(return_value=False)
        mock_db.return_value = iter([mock_session])

        # With a mock user
        mock_user = MagicMock()
        mock_user.user_id = "test-uuid-1234"
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        mock_session.refresh = MagicMock(side_effect=lambda x: setattr(x, "user_id", "test-uuid-1234"))

        with patch("app.api.auth._get_or_create_user", return_value=mock_user):
            with patch("app.api.auth.get_youtube_auth_url", return_value="https://accounts.google.com/oauth"):
                with patch("app.api.auth.get_reddit_auth_url", return_value="https://reddit.com/oauth"):
                    response = client.post(
                        "/api/auth/start",
                        json={"platforms": ["youtube", "reddit"], "historical_fetch": True, "future_sync": True},
                    )
                    assert response.status_code == 200
                    data = response.json()
                    assert "auth_urls" in data
                    assert "session_id" in data


def test_security_encrypt_decrypt():
    """Test token encryption/decryption round-trip."""
    from app.utils.security import encrypt_token, decrypt_token
    original = "my-super-secret-token-12345"
    encrypted = encrypt_token(original)
    assert encrypted != original
    decrypted = decrypt_token(encrypted)
    assert decrypted == original


def test_jwt_create_decode():
    """Test JWT token creation and decoding."""
    from app.utils.security import create_access_token, decode_access_token
    token = create_access_token({"sub": "user-123", "platform": "youtube"})
    assert token is not None
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "user-123"
    assert payload["platform"] == "youtube"


def test_jwt_invalid_token():
    """Test that invalid JWT returns None."""
    from app.utils.security import decode_access_token
    result = decode_access_token("invalid.token.here")
    assert result is None


def test_docs_available():
    """Test that OpenAPI docs are accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
