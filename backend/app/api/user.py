from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import User, OAuthToken, Consent, RawData, SyncLog, OceanScore
from app.schemas.schemas import (
    UserProfileResponse, OceanScoreData, DisconnectResponse, DeleteResponse, DeleteRequest
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


def _latest_ocean(db: Session, user_id, platform: Optional[str] = None) -> Optional[OceanScoreData]:
    q = db.query(OceanScore).filter(OceanScore.user_id == user_id)
    if platform is None:
        q = q.filter(OceanScore.platform == None)
    else:
        q = q.filter(OceanScore.platform == platform)
    score = q.order_by(OceanScore.computed_at.desc()).first()
    if score is None:
        return None
    return OceanScoreData(
        openness=score.openness or 0.0,
        conscientiousness=score.conscientiousness or 0.0,
        extraversion=score.extraversion or 0.0,
        agreeableness=score.agreeableness or 0.0,
        neuroticism=score.neuroticism or 0.0,
        confidence=score.confidence,
        trend=score.trend,
    )


@router.get("/profile", response_model=UserProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return the user's final OCEAN scores and platform-specific scores."""
    final_score = _latest_ocean(db, current_user.user_id, platform=None)
    platforms = {}
    for platform in ["youtube", "reddit"]:
        platforms[platform] = _latest_ocean(db, current_user.user_id, platform=platform)

    last_score = db.query(OceanScore).filter(
        OceanScore.user_id == current_user.user_id
    ).order_by(OceanScore.computed_at.desc()).first()
    last_updated = last_score.computed_at if last_score else None

    return UserProfileResponse(
        user_id=str(current_user.user_id),
        ocean=final_score,
        platforms=platforms,
        last_updated=last_updated,
    )


@router.get("/{platform}/scores", response_model=OceanScoreData)
def get_platform_scores(
    platform: str = Path(..., regex="^(youtube|reddit)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return platform-specific OCEAN scores."""
    score = _latest_ocean(db, current_user.user_id, platform=platform)
    if score is None:
        raise HTTPException(status_code=404, detail=f"No OCEAN scores found for platform: {platform}")
    return score


@router.post("/disconnect/{platform}", response_model=DisconnectResponse)
def disconnect_platform(
    platform: str = Path(..., regex="^(youtube|reddit)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Disconnect a platform by deactivating its OAuth token."""
    token = db.query(OAuthToken).filter(
        OAuthToken.user_id == current_user.user_id,
        OAuthToken.platform == platform,
        OAuthToken.is_active == True,
    ).first()
    if token:
        token.is_active = False
        db.commit()

    # Also update consent
    consent = db.query(Consent).filter(
        Consent.user_id == current_user.user_id, Consent.is_active == True
    ).first()
    if consent and platform in (consent.platforms or []):
        platforms = list(consent.platforms)
        platforms.remove(platform)
        consent.platforms = platforms
        db.commit()

    return DisconnectResponse(
        status="success",
        platform=platform,
        message=f"Successfully disconnected {platform}",
    )


@router.post("/delete", response_model=DeleteResponse)
def request_deletion(
    request: DeleteRequest = DeleteRequest(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete all user data and deactivate account."""
    user_id = current_user.user_id

    # Delete all related data
    db.query(RawData).filter(RawData.user_id == user_id).delete()
    db.query(OceanScore).filter(OceanScore.user_id == user_id).delete()
    db.query(SyncLog).filter(SyncLog.user_id == user_id).delete()
    db.query(OAuthToken).filter(OAuthToken.user_id == user_id).delete()
    db.query(Consent).filter(Consent.user_id == user_id).delete()
    db.query(User).filter(User.user_id == user_id).delete()
    db.commit()

    return DeleteResponse(status="success", message="All user data has been deleted")


@router.post("/revoke-consent", response_model=DeleteResponse)
def revoke_consent(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Revoke all active consents and deactivate OAuth tokens."""
    db.query(Consent).filter(
        Consent.user_id == current_user.user_id, Consent.is_active == True
    ).update({"is_active": False, "revoked_at": datetime.utcnow()})

    db.query(OAuthToken).filter(
        OAuthToken.user_id == current_user.user_id, OAuthToken.is_active == True
    ).update({"is_active": False})

    db.commit()
    return DeleteResponse(status="success", message="All consents have been revoked")
