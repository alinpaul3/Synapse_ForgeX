import httpx
from typing import Dict, Any, Optional
from app.config import settings


async def call_ml_pipeline(user_id: str, platform_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Call Person 3's ML pipeline endpoint with preprocessed platform data.
    Returns OCEAN scores dict or None on failure.
    """
    payload = {
        "user_id": user_id,
        "platform_data": platform_data,
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(settings.ml_pipeline_url, json=payload)
            response.raise_for_status()
            return response.json()
    except Exception:
        return None
