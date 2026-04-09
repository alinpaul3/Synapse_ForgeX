#!/usr/bin/env python3
"""
Test script for load_data.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader.load_data import fetch_user_data
import logging

# Configure logging to see the logger output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_fetch_user_data():
    """Test the fetch_user_data function"""
    print("Testing fetch_user_data function...")

    # Test with the specific user_id you mentioned
    test_user_id = "123"  # This will create: https://archetypal-anthropographic-hana.ngrok-free.dev/processed-data/123

    try:
        print(f"Fetching data for user: {test_user_id}")
        data = fetch_user_data(test_user_id)

        print("✓ Successfully fetched data!")
        print(f"Data type: {type(data)}")

        # Import and use the inspection function
        from inspect_data import inspect_data, demonstrate_data_access

        print("\n--- DATA INSPECTION ---")
        inspect_data(data)

        print("\n--- DATA ACCESS EXAMPLES ---")
        demonstrate_data_access(data)

        return data

    except Exception as e:
        print(f"✗ Failed to fetch data: {e}")
        print("This is expected if the API endpoint is not running or accessible.")
        return None

if __name__ == "__main__":
    print("Running load_data tests...\n")

    result = test_fetch_user_data()

    print("\nTest completed!")

    if result:
        print("The function works! The API returned data.")
    else:
        print("The function encountered an error (likely API not accessible).")
        print("To test properly, make sure your backend API is running at:")
        print("https://archetypal-anthropographic-hana.ngrok-free.dev")