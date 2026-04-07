from typing import List, Dict, Any

try:
    import praw
    _praw_available = True
except ImportError:
    _praw_available = False

from app.config import settings
from app.utils.security import decrypt_token
from app.models.models import OAuthToken


def get_reddit_instance(token: OAuthToken) -> Any:
    """Build an authenticated PRAW Reddit instance from a stored OAuth token."""
    if not _praw_available:
        raise RuntimeError("praw is not installed")
    access_token = decrypt_token(token.access_token_encrypted)
    reddit = praw.Reddit(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        user_agent=settings.reddit_user_agent,
    )
    reddit._core._authorizer._access_token = access_token
    return reddit


def fetch_reddit_posts(reddit: Any, username: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Fetch submitted posts for a Reddit user."""
    posts = []
    try:
        user = reddit.redditor(username)
        for submission in user.submissions.new(limit=limit):
            posts.append({
                "post_id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "subreddit": str(submission.subreddit),
                "score": submission.score,
                "num_comments": submission.num_comments,
                "created_utc": submission.created_utc,
                "url": submission.url,
            })
    except Exception:
        pass
    return posts


def fetch_reddit_comments(reddit: Any, username: str, limit: int = 200) -> List[Dict[str, Any]]:
    """Fetch comments for a Reddit user."""
    comments = []
    try:
        user = reddit.redditor(username)
        for comment in user.comments.new(limit=limit):
            comments.append({
                "comment_id": comment.id,
                "body": comment.body,
                "subreddit": str(comment.subreddit),
                "score": comment.score,
                "created_utc": comment.created_utc,
                "link_id": comment.link_id,
            })
    except Exception:
        pass
    return comments


def fetch_reddit_identity(reddit: Any) -> Dict[str, Any]:
    """Fetch the authenticated Reddit user's basic info."""
    try:
        me = reddit.user.me()
        return {
            "username": me.name,
            "karma": me.link_karma + me.comment_karma,
            "created_utc": me.created_utc,
            "is_verified": me.verified,
        }
    except Exception:
        return {}
