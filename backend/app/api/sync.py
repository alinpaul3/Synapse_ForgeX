import asyncio
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import User, OAuthToken, RawData, SyncLog
from app.schemas.schemas import SyncRequest, SyncResponse, SyncStatusResponse
from app.services.youtube import get_youtube_credentials, fetch_youtube_channel, fetch_youtube_videos, fetch_youtube_comments
from app.services.reddit import get_reddit_instance, fetch_reddit_identity, fetch_reddit_posts, fetch_reddit_comments
from app.services.ml_client import call_ml_pipeline
from app.utils.dependencies import get_current_user
from app.models.models import OceanScore

router = APIRouter(prefix="/sync", tags=["sync"])


def _run_youtube_sync(user_id: str, historical: bool, db: Session) -> None:
    """Background task: fetch YouTube data and store it."""
    log = SyncLog(user_id=user_id, platform="youtube", sync_type="historical" if historical else "incremental", status="syncing")
    db.add(log)
    db.commit()
    db.refresh(log)

    try:
        token = db.query(OAuthToken).filter(
            OAuthToken.user_id == user_id, OAuthToken.platform == "youtube", OAuthToken.is_active == True
        ).first()
        if token is None:
            raise ValueError("No active YouTube token")

        credentials = get_youtube_credentials(token)
        channel = fetch_youtube_channel(credentials)
        count = 0

        if channel:
            # Store channel data
            rd = RawData(user_id=user_id, platform="youtube", data_type="channel",
                         content=channel.get("description", ""), metadata_json=channel)
            db.add(rd)
            count += 1

            videos = fetch_youtube_videos(credentials, channel["channel_id"], max_results=50 if historical else 10)
            for video in videos:
                rd = RawData(user_id=user_id, platform="youtube", data_type="video",
                             content=f"{video.get('title', '')} {video.get('description', '')}",
                             metadata_json=video, external_id=video.get("video_id"),
                             timestamp=datetime.fromisoformat(video["published_at"].rstrip("Z")) if video.get("published_at") else None)
                db.add(rd)
                count += 1

                # Fetch comments for each video
                comments = fetch_youtube_comments(credentials, video["video_id"], max_results=20)
                for comment in comments:
                    rd = RawData(user_id=user_id, platform="youtube", data_type="comment",
                                 content=comment.get("text", ""),
                                 metadata_json=comment, external_id=comment.get("comment_id"),
                                 timestamp=datetime.fromisoformat(comment["published_at"].rstrip("Z")) if comment.get("published_at") else None)
                    db.add(rd)
                    count += 1

        db.commit()
        log.status = "completed"
        log.completed_at = datetime.utcnow()
        log.data_count = count
        db.commit()

    except Exception as e:
        log.status = "failed"
        log.error_message = str(e)
        log.completed_at = datetime.utcnow()
        db.commit()


def _run_reddit_sync(user_id: str, historical: bool, db: Session) -> None:
    """Background task: fetch Reddit data and store it."""
    log = SyncLog(user_id=user_id, platform="reddit", sync_type="historical" if historical else "incremental", status="syncing")
    db.add(log)
    db.commit()
    db.refresh(log)

    try:
        token = db.query(OAuthToken).filter(
            OAuthToken.user_id == user_id, OAuthToken.platform == "reddit", OAuthToken.is_active == True
        ).first()
        if token is None:
            raise ValueError("No active Reddit token")

        reddit = get_reddit_instance(token)
        identity = fetch_reddit_identity(reddit)
        username = identity.get("username", "")
        count = 0

        if username:
            posts = fetch_reddit_posts(reddit, username, limit=100 if historical else 10)
            for post in posts:
                from datetime import timezone
                ts = datetime.fromtimestamp(post["created_utc"], tz=timezone.utc).replace(tzinfo=None) if post.get("created_utc") else None
                rd = RawData(user_id=user_id, platform="reddit", data_type="post",
                             content=f"{post.get('title', '')} {post.get('selftext', '')}",
                             metadata_json=post, external_id=post.get("post_id"), timestamp=ts)
                db.add(rd)
                count += 1

            comments = fetch_reddit_comments(reddit, username, limit=200 if historical else 20)
            for comment in comments:
                from datetime import timezone
                ts = datetime.fromtimestamp(comment["created_utc"], tz=timezone.utc).replace(tzinfo=None) if comment.get("created_utc") else None
                rd = RawData(user_id=user_id, platform="reddit", data_type="comment",
                             content=comment.get("body", ""),
                             metadata_json=comment, external_id=comment.get("comment_id"), timestamp=ts)
                db.add(rd)
                count += 1

        db.commit()
        log.status = "completed"
        log.completed_at = datetime.utcnow()
        log.data_count = count
        db.commit()

    except Exception as e:
        log.status = "failed"
        log.error_message = str(e)
        log.completed_at = datetime.utcnow()
        db.commit()


@router.post("/{platform}", response_model=SyncResponse)
def trigger_sync(
    platform: str = Path(..., regex="^(youtube|reddit)$"),
    request: SyncRequest = SyncRequest(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Trigger a data sync for the specified platform."""
    token = db.query(OAuthToken).filter(
        OAuthToken.user_id == current_user.user_id,
        OAuthToken.platform == platform,
        OAuthToken.is_active == True,
    ).first()
    if token is None:
        raise HTTPException(status_code=400, detail=f"No active {platform} connection. Please authenticate first.")

    if platform == "youtube":
        background_tasks.add_task(_run_youtube_sync, str(current_user.user_id), request.historical, db)
    else:
        background_tasks.add_task(_run_reddit_sync, str(current_user.user_id), request.historical, db)

    # Return most recent log id as job_id
    log = db.query(SyncLog).filter(
        SyncLog.user_id == current_user.user_id, SyncLog.platform == platform
    ).order_by(SyncLog.started_at.desc()).first()
    job_id = str(log.log_id) if log else "pending"

    return SyncResponse(status="syncing", job_id=job_id, platform=platform)


@router.get("/{job_id}", response_model=SyncStatusResponse)
def get_sync_status(
    job_id: str = Path(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Check the status of a sync job."""
    log = db.query(SyncLog).filter(
        SyncLog.log_id == job_id,
        SyncLog.user_id == current_user.user_id,
    ).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Sync job not found")

    return SyncStatusResponse(
        status=log.status,
        platform=log.platform,
        data_count=log.data_count or 0,
        started_at=log.started_at,
        completed_at=log.completed_at,
        error_message=log.error_message,
    )
