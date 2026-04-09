#!/usr/bin/env python3
"""
Test script for SchemaValidator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader.validate_schema import SchemaValidator

def test_dataframe_validation():
    """Test DataFrame-like validation"""
    print("Testing DataFrame validation...")

    # Mock DataFrame-like object
    class MockDataFrame:
        def __init__(self, columns, data):
            self.columns = columns
            self.data = data

        def __len__(self):
            return len(self.data)

        def __getitem__(self, col):
            return MockSeries([row[self.columns.index(col)] for row in self.data])

    class MockSeries:
        def __init__(self, data):
            self.data = data
            self.dtype = type(data[0]).__name__ if data else 'object'

    # Create validator for DataFrame
    validator = SchemaValidator(
        required_columns=['user_id', 'text'],
        column_types={'user_id': 'str', 'text': 'str'},
        min_rows=1
    )

    # Test valid DataFrame
    df = MockDataFrame(
        columns=['user_id', 'text'],
        data=[['user1', 'hello world'], ['user2', 'test message']]
    )

    try:
        result = validator.validate(df)
        print("✓ DataFrame validation passed")
    except Exception as e:
        print(f"✗ DataFrame validation failed: {e}")

def test_nested_record_validation():
    """Test nested JSON record validation"""
    print("\nTesting nested record validation...")

    # Create validator (no required columns for record validation)
    validator = SchemaValidator()

    # Valid record
    valid_record = {
        "user_id": "user123",
        "platform": "twitter",
        "cleaned_text": ["Hello world", "This is a test"],
        "timestamps": [1640995200.0, 1640995260.0],
        "metadata": {
            "word_count": 5,
            "sentiment_score": 0.8,
            "hashtags": ["#test", "#demo"],
            "nested": {"key": "value"}
        }
    }

    try:
        result = validator.validate(valid_record)
        print("✓ Single record validation passed")
    except Exception as e:
        print(f"✗ Single record validation failed: {e}")

    # Test list of records
    records = [valid_record, valid_record.copy()]

    try:
        result = validator.validate(records)
        print("✓ List of records validation passed")
    except Exception as e:
        print(f"✗ List of records validation failed: {e}")

def test_invalid_record():
    """Test invalid record validation"""
    print("\nTesting invalid record validation...")

    validator = SchemaValidator()

    # Invalid record - missing required key
    invalid_record = {
        "user_id": "user123",
        "platform": "twitter",
        "cleaned_text": ["Hello world"],
        "timestamps": [1640995200.0],
        # missing metadata
    }

    try:
        result = validator.validate(invalid_record)
        print("✗ Invalid record should have failed but passed")
    except ValueError as e:
        print(f"✓ Invalid record correctly failed: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

if __name__ == "__main__":
    print("Running SchemaValidator tests...\n")

    test_dataframe_validation()
    test_nested_record_validation()
    test_invalid_record()

    print("\nAll tests completed!")