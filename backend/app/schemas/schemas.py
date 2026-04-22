from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr
import uuid


# Auth schemas
class AuthStartRequest(BaseModel):
    platforms: List[str]
    historical_fetch: bool = True
    future_sync: bool = True


class AuthStartResponse(BaseModel):
    auth_urls: Dict[str, str]
    session_id: str


class AuthCallbackResponse(BaseModel):
    status: str
    user_id: str
    token: str
    platform: str


# Consent schemas
class ConsentCreate(BaseModel):
    platforms: List[str]
    historical_allowed: bool
    sync_allowed: bool


class ConsentResponse(BaseModel):
    consent_id: str
    platforms: List[str]
    historical_allowed: bool
    sync_allowed: bool
    agreed_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# Sync schemas
class SyncRequest(BaseModel):
    historical: bool = False


class SyncResponse(BaseModel):
    status: str
    job_id: str
    platform: str


class SyncStatusResponse(BaseModel):
    status: str
    platform: str
    data_count: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]

    class Config:
        from_attributes = True


# OCEAN score schemas
class OceanScoreData(BaseModel):
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float
    confidence: Optional[float] = None
    trend: Optional[str] = None

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    user_id: str
    ocean: Optional[OceanScoreData]
    platforms: Dict[str, Optional[OceanScoreData]]
    last_updated: Optional[datetime]

    class Config:
        from_attributes = True


# User schemas
class UserResponse(BaseModel):
    user_id: str
    email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DeleteRequest(BaseModel):
    reason: Optional[str] = None


class DisconnectResponse(BaseModel):
    status: str
    platform: str
    message: str


class DeleteResponse(BaseModel):
    status: str
    message: str
