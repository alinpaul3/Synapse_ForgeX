import re
import numpy as np

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def process_data(input_data):
    raw_data = input_data.get("data", [])

    if not raw_data:
        return {}

    cleaned_text = []
    timestamps = []
    categories = []

    for item in raw_data:
        text = item.get("commentText", "")
        timestamp = item.get("timestamp", "")
        category = item.get("videoCategory", "")

        if text:
            cleaned_text.append(clean_text(text))

        if timestamp:
            timestamps.append(timestamp)

        if category:
            categories.append(category)

    num_comments = len(cleaned_text)

    avg_length = np.mean([len(t) for t in cleaned_text]) if cleaned_text else 0

    unique_categories = len(set(categories))

    metadata = {
        "num_comments": num_comments,
        "avg_length": avg_length,
        "unique_categories": unique_categories
    }

    return {
        "user_id": input_data.get("user_id"),
        "platform": input_data.get("platform"),
        "cleaned_text": cleaned_text,
        "timestamps": timestamps,
        "metadata": metadata
    }