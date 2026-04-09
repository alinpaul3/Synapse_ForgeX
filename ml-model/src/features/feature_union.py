"""
Combine all feature types into one ML-ready structure.
"""

from typing import Dict, Any

from .metadata_features import build_metadata_features
from .time_features import build_time_features
from .platform_features import encode_platform
from .text_vectorizer import combine_text


def build_features(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build all features from one validated real-data record.
    """
    combined_text = combine_text(record["cleaned_text"])
    metadata_features = build_metadata_features(record["metadata"])
    time_features = build_time_features(record["timestamps"])
    platform_features = encode_platform(record["platform"])

    return {
        "user_id": record["user_id"],
        "platform": record["platform"],
        "text": combined_text,
        "metadata_features": metadata_features,
        "time_features": time_features,
        "platform_features": platform_features,
    }


if __name__ == "__main__":
    from src.data_loader.load_data import fetch_user_data

    request = {
        "user_id": "123"
    }

    data = fetch_user_data(request["user_id"])
    features = build_features(data)

    print("Combined ML-ready features:")
    print(features)