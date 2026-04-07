import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text, Float, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import types as sa_types
from sqlalchemy.orm import relationship
from app.db import Base


class GUID(sa_types.TypeDecorator):
    """Platform-independent UUID type. Uses PostgreSQL UUID natively, String(36) for SQLite."""
    impl = sa_types.String(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(sa_types.String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid.UUID(str(value))


class User(Base):
    __tablename__ = "users"

    user_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    consents = relationship("Consent", back_populates="user", cascade="all, delete-orphan")
    sync_logs = relationship("SyncLog", back_populates="user", cascade="all, delete-orphan")
    raw_data = relationship("RawData", back_populates="user", cascade="all, delete-orphan")
    ocean_scores = relationship("OceanScore", back_populates="user", cascade="all, delete-orphan")
    oauth_tokens = relationship("OAuthToken", back_populates="user", cascade="all, delete-orphan")


class Consent(Base):
    __tablename__ = "consents"

    consent_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    platforms = Column(JSON, default=list)
    historical_allowed = Column(Boolean, default=False)
    sync_allowed = Column(Boolean, default=False)
    agreed_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="consents")


class OAuthToken(Base):
    __tablename__ = "oauth_tokens"

    token_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)
    access_token_encrypted = Column(Text, nullable=False)
    refresh_token_encrypted = Column(Text, nullable=True)
    token_expiry = Column(DateTime, nullable=True)
    scope = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="oauth_tokens")


class SyncLog(Base):
    __tablename__ = "sync_logs"

    log_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)
    sync_type = Column(String(20), default="incremental")  # historical or incremental
    status = Column(String(20), default="pending")  # pending, syncing, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    data_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

    user = relationship("User", back_populates="sync_logs")


class RawData(Base):
    __tablename__ = "raw_data"

    data_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)
    data_type = Column(String(50), nullable=False)  # comment, post, video, caption
    content = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    external_id = Column(String(255), nullable=True)
    timestamp = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="raw_data")


class OceanScore(Base):
    __tablename__ = "ocean_scores"

    score_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=True)  # null means fused/final score
    openness = Column(Float, nullable=True)
    conscientiousness = Column(Float, nullable=True)
    extraversion = Column(Float, nullable=True)
    agreeableness = Column(Float, nullable=True)
    neuroticism = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    trend = Column(String(20), nullable=True)  # increasing, decreasing, stable
    model_version = Column(String(50), nullable=True)
    computed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ocean_scores")
