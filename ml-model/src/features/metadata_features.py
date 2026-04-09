"""
Metadata feature extraction.
"""

from typing import Any, Dict, List


def build_metadata_features(metadata: Dict[str, Any]) -> List[float]:
    """
    Convert metadata dictionary into an ordered numeric feature list.
    """
    return [
        float(metadata["num_comments"]),
        float(metadata["avg_length"]),
        float(metadata["avg_score"]),
        float(metadata["avg_replies"]),
        float(metadata["unique_subreddits"]),
    ]


from src.data_loader.load_data import fetch_user_data

if __name__ == "__main__":
    request = {
    "user_id": "123" #dummy user_id for testing
    }
    data = fetch_user_data(request["user_id"])   # real API call

    metadata = data["metadata"]

    print(build_metadata_features(metadata))