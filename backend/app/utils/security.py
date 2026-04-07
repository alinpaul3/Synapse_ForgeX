import base64
import os
from datetime import datetime, timedelta
from typing import Optional
from cryptography.fernet import Fernet
from jose import JWTError, jwt
from app.config import settings


def get_fernet_key() -> bytes:
    """Derive a valid Fernet key from the configured encryption key."""
    key = settings.encryption_key.encode()
    # Pad or trim to 32 bytes and base64-encode for Fernet
    key = key[:32].ljust(32, b"=")
    return base64.urlsafe_b64encode(key)


_fernet = None


def get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        _fernet = Fernet(get_fernet_key())
    return _fernet


def encrypt_token(token: str) -> str:
    """Encrypt a sensitive token string."""
    return get_fernet().encrypt(token.encode()).decode()


def decrypt_token(encrypted: str) -> str:
    """Decrypt a previously encrypted token string."""
    return get_fernet().decrypt(encrypted.encode()).decode()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT access token. Returns None if invalid."""
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None
