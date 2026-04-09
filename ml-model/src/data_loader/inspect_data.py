#!/usr/bin/env python3
"""
Example of what the data looks like and how to inspect it
"""

import json

# Example data structure that your API should return
sample_data = {
    "user_id": "user123",
    "platform": "twitter",
    "cleaned_text": [
        "Hello world this is my first post",
        "Having a great day today",
        "Just finished an amazing project"
    ],
    "timestamps": [
        1640995200.0,  # Unix timestamp
        1640998800.0,  # Another timestamp
        1641002400.0   # Another timestamp
    ],
    "metadata": {
        "total_posts": 3,
        "word_count": 15,
        "sentiment_score": 0.8,
        "hashtags": ["#hello", "#project"],
        "language": "en",
        "engagement": {
            "likes": 25,
            "retweets": 5,
            "replies": 2
        }
    }
}

def inspect_data(data):
    """Function to inspect and display data structure"""
    print("=== DATA INSPECTION ===")
    print(f"Data type: {type(data)}")
    print(f"Is dictionary: {isinstance(data, dict)}")
    print()

    if isinstance(data, dict):
        print(f"Top-level keys: {list(data.keys())}")
        print()

        # Inspect each key
        for key, value in data.items():
            print(f"--- {key.upper()} ---")
            print(f"Type: {type(value)}")

            if isinstance(value, list):
                print(f"Length: {len(value)}")
                if value and len(value) > 0:
                    print(f"First item type: {type(value[0])}")
                    print(f"Sample items: {value[:3]}")
            elif isinstance(value, dict):
                print(f"Keys: {list(value.keys())}")
                print(f"Sample content: {dict(list(value.items())[:3])}")
            else:
                print(f"Value: {value}")

            print()

    # Pretty print full data
    print("=== FULL DATA (JSON) ===")
    print(json.dumps(data, indent=2))

def demonstrate_data_access(data):
    """Show how to access different parts of the data"""
    print("\n=== DATA ACCESS EXAMPLES ===")

    # Access basic fields
    user_id = data.get("user_id")
    platform = data.get("platform")
    print(f"User ID: {user_id}")
    print(f"Platform: {platform}")

    # Access lists
    cleaned_text = data.get("cleaned_text", [])
    print(f"Number of text entries: {len(cleaned_text)}")
    print(f"First text: {cleaned_text[0] if cleaned_text else 'None'}")

    # Access timestamps
    timestamps = data.get("timestamps", [])
    print(f"Number of timestamps: {len(timestamps)}")

    # Access nested metadata
    metadata = data.get("metadata", {})
    sentiment = metadata.get("sentiment_score")
    total_posts = metadata.get("total_posts")
    print(f"Sentiment score: {sentiment}")
    print(f"Total posts: {total_posts}")

    # Access deeply nested data
    engagement = metadata.get("engagement", {})
    likes = engagement.get("likes")
    print(f"Likes: {likes}")

if __name__ == "__main__":
    print("This shows what your API data should look like:\n")

    inspect_data(sample_data)
    demonstrate_data_access(sample_data)

    print("\n" + "="*50)
    print("When your API is running, replace 'sample_data' with:")
    print("data = fetch_user_data('actual_user_id')")
    print("Then call inspect_data(data) and demonstrate_data_access(data)")