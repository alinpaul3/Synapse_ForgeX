from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    _google_available = True
except ImportError:
    _google_available = False
    Credentials = None  # type: ignore[assignment,misc]

from app.utils.security import decrypt_token
from app.models.models import OAuthToken
from sqlalchemy.orm import Session


def get_youtube_credentials(token: OAuthToken) -> Any:
    """Build Google credentials from a stored OAuth token."""
    if not _google_available:
        raise RuntimeError("google-api-python-client is not installed")
    access_token = decrypt_token(token.access_token_encrypted)
    refresh_token = decrypt_token(token.refresh_token_encrypted) if token.refresh_token_encrypted else None
    from app.config import settings
    return Credentials(  # type: ignore[misc]
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.youtube_client_id,
        client_secret=settings.youtube_client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.readonly"],
    )


def fetch_youtube_channel(credentials: Any) -> Optional[Dict[str, Any]]:
    """Fetch the authenticated user's YouTube channel info."""
    if not _google_available:
        return None
    youtube = build("youtube", "v3", credentials=credentials)
    response = youtube.channels().list(part="snippet,statistics", mine=True).execute()
    items = response.get("items", [])
    if not items:
        return None
    channel = items[0]
    return {
        "channel_id": channel["id"],
        "title": channel["snippet"].get("title"),
        "description": channel["snippet"].get("description"),
        "subscriber_count": channel["statistics"].get("subscriberCount"),
        "video_count": channel["statistics"].get("videoCount"),
    }


def fetch_youtube_videos(credentials: Any, channel_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
    """Fetch uploaded videos for the channel."""
    if not _google_available:
        return []
    youtube = build("youtube", "v3", credentials=credentials)
    videos = []

    # Get uploads playlist
    response = youtube.channels().list(part="contentDetails", id=channel_id).execute()
    items = response.get("items", [])
    if not items:
        return videos
    uploads_playlist_id = items[0]["contentDetails"]["relatedPlaylists"].get("uploads")
    if not uploads_playlist_id:
        return videos

    next_page_token = None
    while True:
        pl_response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=min(max_results - len(videos), 50),
            pageToken=next_page_token,
        ).execute()

        for item in pl_response.get("items", []):
            videos.append({
                "video_id": item["contentDetails"]["videoId"],
                "title": item["snippet"].get("title"),
                "description": item["snippet"].get("description"),
                "published_at": item["snippet"].get("publishedAt"),
            })

        next_page_token = pl_response.get("nextPageToken")
        if not next_page_token or len(videos) >= max_results:
            break

    return videos


def fetch_youtube_comments(credentials: Any, video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
    """Fetch top-level comments for a YouTube video."""
    if not _google_available:
        return []
    youtube = build("youtube", "v3", credentials=credentials)
    comments = []
    next_page_token = None

    while True:
        try:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(max_results - len(comments), 100),
                pageToken=next_page_token,
                textFormat="plainText",
            ).execute()
        except Exception:
            break

        for item in response.get("items", []):
            top = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "comment_id": item["id"],
                "text": top.get("textDisplay"),
                "author": top.get("authorDisplayName"),
                "like_count": top.get("likeCount"),
                "published_at": top.get("publishedAt"),
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token or len(comments) >= max_results:
            break

    return comments
