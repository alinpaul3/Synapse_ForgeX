"""
Time-based feature extraction.
Builds simple numeric features from real timestamp data.
"""

from typing import List
from datetime import datetime


def build_time_features(timestamps: List[float]) -> List[float]:
    """
    Build time-based features from a list of Unix timestamps.

    Returns a list:
    [
        num_posts,
        activity_span_seconds,
        posting_rate,
        avg_gap_seconds,
        night_activity_ratio,
        weekend_activity_ratio
    ]
    """
    if not timestamps:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # convert all timestamps to float and sort
    ts = sorted(float(t) for t in timestamps)

    num_posts = float(len(ts))

    # span
    if len(ts) > 1:
        activity_span = float(ts[-1] - ts[0])
        posting_rate = float(len(ts) / (activity_span + 1))
        gaps = [ts[i] - ts[i - 1] for i in range(1, len(ts))]
        avg_gap = float(sum(gaps) / len(gaps))
    else:
        activity_span = 0.0
        posting_rate = 1.0
        avg_gap = 0.0

    # time-of-day / weekend behavior
    night_count = 0
    weekend_count = 0

    for t in ts:
        dt = datetime.fromtimestamp(t)
        hour = dt.hour
        weekday = dt.weekday()  # Monday=0, Sunday=6

        if hour >= 22 or hour < 6:
            night_count += 1

        if weekday >= 5:
            weekend_count += 1

    night_activity_ratio = float(night_count / len(ts))
    weekend_activity_ratio = float(weekend_count / len(ts))

    return [
        num_posts,
        activity_span,
        posting_rate,
        avg_gap,
        night_activity_ratio,
        weekend_activity_ratio,
    ]


if __name__ == "__main__":
    from src.data_loader.load_data import fetch_user_data

    request = {
        "user_id": "123"
    }

    data = fetch_user_data(request["user_id"])
    timestamps = data["timestamps"]

    features = build_time_features(timestamps)
    print(features)