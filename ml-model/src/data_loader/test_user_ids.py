#!/usr/bin/env python3
"""
Examples of different user_id formats you might use
"""

def test_different_user_ids():
    """Test the function with different user_id formats"""

    from data_loader.load_data import fetch_user_data
    import logging
    logging.basicConfig(level=logging.INFO)

    # Common user_id formats
    test_user_ids = [
        "123",                    # Simple numeric ID
        "user123",               # Prefixed numeric
        "john_doe",              # Username style
        "550e8400-e29b-41d4-a716-446655440000",  # UUID
        "@johndoe",              # Social media handle
        "twitter_12345",         # Platform-specific ID
    ]

    print("Testing different user_id formats:")
    print("=" * 50)

    for user_id in test_user_ids:
        print(f"\nTesting user_id: '{user_id}'")
        print(f"Generated URL: https://archetypal-anthropographic-hana.ngrok-free.dev/processed-data/{user_id}")

        try:
            data = fetch_user_data(user_id)
            print("✅ Success! Data fetched.")
            print(f"   User ID in response: {data.get('user_id', 'N/A')}")
        except Exception as e:
            print(f"❌ Failed: {e}")

        print("-" * 30)

if __name__ == "__main__":
    test_different_user_ids()