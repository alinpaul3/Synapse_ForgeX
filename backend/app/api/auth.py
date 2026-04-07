import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import User, Consent, OAuthToken
from app.schemas.schemas import AuthStartRequest, AuthStartResponse, AuthCallbackResponse
from app.services.oauth import (
    get_youtube_auth_url, exchange_youtube_code,
    get_reddit_auth_url, exchange_reddit_code,
)
from app.utils.security import encrypt_token, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


def _get_or_create_user(db: Session) -> User:
    """Create a new anonymous user and persist it."""
    user = User()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/start", response_model=AuthStartResponse)
def start_auth(request: AuthStartRequest, db: Session = Depends(get_db)):
    """
    Start the OAuth flow for selected platforms.
    Creates a new user record and returns OAuth authorization URLs.
    """
    user = _get_or_create_user(db)

    # Store consent
    consent = Consent(
        user_id=user.user_id,
        platforms=request.platforms,
        historical_allowed=request.historical_fetch,
        sync_allowed=request.future_sync,
    )
    db.add(consent)
    db.commit()

    auth_urls = {}
    user_id_str = str(user.user_id)

    if "youtube" in request.platforms:
        try:
            auth_urls["youtube"] = get_youtube_auth_url(user_id_str)
        except Exception:
            auth_urls["youtube"] = ""

    if "reddit" in request.platforms:
        try:
            auth_urls["reddit"] = get_reddit_auth_url(user_id_str)
        except Exception:
            auth_urls["reddit"] = ""

    return AuthStartResponse(auth_urls=auth_urls, session_id=user_id_str)


@router.get("/youtube/authorize")
def youtube_authorize(user_id: str = Query(...), db: Session = Depends(get_db)):
    """Return YouTube OAuth authorization URL for the given user."""
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    auth_url = get_youtube_auth_url(str(user.user_id))
    return {"auth_url": auth_url}


@router.get("/youtube/callback", response_model=AuthCallbackResponse)
def youtube_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db),
):
    """Handle YouTube OAuth2 callback."""
    token_dict, user_id = exchange_youtube_code(code, state)
    if token_dict is None or user_id is None:
        raise HTTPException(status_code=400, detail="Invalid OAuth state or code")

    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Store encrypted tokens
    existing = db.query(OAuthToken).filter(
        OAuthToken.user_id == user.user_id, OAuthToken.platform == "youtube"
    ).first()
    if existing:
        existing.access_token_encrypted = encrypt_token(token_dict["access_token"])
        if token_dict.get("refresh_token"):
            existing.refresh_token_encrypted = encrypt_token(token_dict["refresh_token"])
        existing.updated_at = datetime.utcnow()
        existing.is_active = True
    else:
        oauth_token = OAuthToken(
            user_id=user.user_id,
            platform="youtube",
            access_token_encrypted=encrypt_token(token_dict["access_token"]),
            refresh_token_encrypted=encrypt_token(token_dict["refresh_token"]) if token_dict.get("refresh_token") else None,
            scope=token_dict.get("scope"),
        )
        db.add(oauth_token)

    db.commit()

    jwt_token = create_access_token({"sub": str(user.user_id), "platform": "youtube"})
    return AuthCallbackResponse(
        status="success",
        user_id=str(user.user_id),
        token=jwt_token,
        platform="youtube",
    )


@router.get("/reddit/authorize")
def reddit_authorize(user_id: str = Query(...), db: Session = Depends(get_db)):
    """Return Reddit OAuth authorization URL for the given user."""
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    auth_url = get_reddit_auth_url(str(user.user_id))
    return {"auth_url": auth_url}


@router.get("/reddit/callback", response_model=AuthCallbackResponse)
def reddit_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db),
):
    """Handle Reddit OAuth2 callback."""
    token_dict, user_id = exchange_reddit_code(code, state)
    if token_dict is None or user_id is None:
        raise HTTPException(status_code=400, detail="Invalid OAuth state or code")

    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(OAuthToken).filter(
        OAuthToken.user_id == user.user_id, OAuthToken.platform == "reddit"
    ).first()
    if existing:
        existing.access_token_encrypted = encrypt_token(token_dict["access_token"])
        existing.updated_at = datetime.utcnow()
        existing.is_active = True
    else:
        oauth_token = OAuthToken(
            user_id=user.user_id,
            platform="reddit",
            access_token_encrypted=encrypt_token(token_dict["access_token"]),
            scope=token_dict.get("scope"),
        )
        db.add(oauth_token)

    db.commit()

    jwt_token = create_access_token({"sub": str(user.user_id), "platform": "reddit"})
    return AuthCallbackResponse(
        status="success",
        user_id=str(user.user_id),
        token=jwt_token,
        platform="reddit",
    )
