"""
Platform-based feature extraction.
Encodes the platform into numeric features for the model.
"""

from typing import List


SUPPORTED_PLATFORMS = ["reddit", "youtube"]


def encode_platform(platform: str) -> List[float]:
    """
    One-hot encode the platform.

    reddit  -> [1.0, 0.0]
    youtube -> [0.0, 1.0]

    If an unknown platform comes in, returns all zeros.
    """
    if not platform:
        return [0.0] * len(SUPPORTED_PLATFORMS)

    platform = platform.strip().lower()
    return [1.0 if platform == p else 0.0 for p in SUPPORTED_PLATFORMS]


if __name__ == "__main__":
    print("reddit  ->", encode_platform("reddit"))
    print("youtube ->", encode_platform("youtube"))
    print("unknown ->", encode_platform("twitter"))