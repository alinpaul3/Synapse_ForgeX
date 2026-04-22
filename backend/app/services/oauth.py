import secrets
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta

try:
    from google_auth_oauthlib.flow import Flow
    _google_available = True
except ImportError:
    _google_available = False

try:
    import praw
    _praw_available = True
except ImportError:
    _praw_available = False

from app.config import settings


YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]

REDDIT_SCOPES = ["identity", "history", "read"]

# In-memory state store (use Redis in production)
_state_store: Dict[str, dict] = {}


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def store_state(state: str, data: dict) -> None:
    _state_store[state] = data


def consume_state(state: str) -> Optional[dict]:
    return _state_store.pop(state, None)


def get_youtube_auth_url(user_id: str) -> str:
    """Generate YouTube OAuth2 authorization URL."""
    if not _google_available:
        raise RuntimeError("google-auth-oauthlib is not installed")
    client_config = {
        "web": {
            "client_id": settings.youtube_client_id,
            "client_secret": settings.youtube_client_secret,
            "redirect_uris": [settings.youtube_redirect_uri],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    flow = Flow.from_client_config(client_config, scopes=YOUTUBE_SCOPES)
    flow.redirect_uri = settings.youtube_redirect_uri

    state = generate_state()
    store_state(state, {"user_id": user_id, "platform": "youtube"})

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        state=state,
        prompt="consent",
    )
    return auth_url


def exchange_youtube_code(code: str, state: str) -> Tuple[Optional[dict], Optional[str]]:
    """Exchange YouTube auth code for tokens. Returns (token_dict, user_id) or (None, None)."""
    if not _google_available:
        raise RuntimeError("google-auth-oauthlib is not installed")
    state_data = consume_state(state)
    if state_data is None:
        return None, None

    client_config = {
        "web": {
            "client_id": settings.youtube_client_id,
            "client_secret": settings.youtube_client_secret,
            "redirect_uris": [settings.youtube_redirect_uri],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    flow = Flow.from_client_config(client_config, scopes=YOUTUBE_SCOPES, state=state)
    flow.redirect_uri = settings.youtube_redirect_uri
    flow.fetch_token(code=code)

    credentials = flow.credentials
    token_dict = {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_expiry": (datetime.utcnow() + timedelta(seconds=3600)).isoformat(),
        "scope": " ".join(YOUTUBE_SCOPES),
    }
    return token_dict, state_data["user_id"]


def get_reddit_auth_url(user_id: str) -> str:
    """Generate Reddit OAuth2 authorization URL."""
    if not _praw_available:
        raise RuntimeError("praw is not installed")
    reddit = praw.Reddit(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        redirect_uri=settings.reddit_redirect_uri,
        user_agent=settings.reddit_user_agent,
    )
    state = generate_state()
    store_state(state, {"user_id": user_id, "platform": "reddit"})
    return reddit.auth.url(scopes=REDDIT_SCOPES, state=state, duration="permanent")


def exchange_reddit_code(code: str, state: str) -> Tuple[Optional[dict], Optional[str]]:
    """Exchange Reddit auth code for tokens. Returns (token_dict, user_id) or (None, None)."""
    if not _praw_available:
        raise RuntimeError("praw is not installed")
    state_data = consume_state(state)
    if state_data is None:
        return None, None

    reddit = praw.Reddit(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        redirect_uri=settings.reddit_redirect_uri,
        user_agent=settings.reddit_user_agent,
    )
    reddit.auth.authorize(code)
    token_dict = {
        "access_token": reddit.auth.access_token(),
        "refresh_token": "",
        "token_expiry": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        "scope": " ".join(REDDIT_SCOPES),
    }
    return token_dict, state_data["user_id"]
