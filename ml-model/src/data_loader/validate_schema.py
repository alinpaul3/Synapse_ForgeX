"""
Schema validation for input data.
"""

from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class SchemaValidator:
    """Validates tabular data and nested JSON record schemas."""

    REQUIRED_RECORD_KEYS = [
        "user_id",
        "platform",
        "cleaned_text",
        "timestamps",
        "metadata",
    ]
    ALLOWED_PLATFORMS = {"twitter", "facebook", "instagram", "linkedin", "reddit"}

    def __init__(
        self,
        required_columns: Optional[List[str]] = None,
        column_types: Optional[Dict[str, str]] = None,
        min_rows: int = 1,
    ):
        """
        Initialize schema validator.

        Args:
            required_columns: List of required column names for DataFrame validation
            column_types: Dict mapping column names to expected types for DataFrame validation
            min_rows: Minimum number of rows required
        """
        self.required_columns = required_columns or []
        self.column_types = column_types or {}
        self.min_rows = min_rows

    def validate(self, data: Any) -> bool:
        """
        Validate data.

        Supports:
        - pandas DataFrame-like objects
        - single nested records (dict)
        - list of nested records

        Args:
            data: Data to validate

        Returns:
            True if valid, raises exception otherwise
        """
        if isinstance(data, dict):
            errors = self.validate_record(data)
            if errors:
                raise ValueError("Record validation failed: " + "; ".join(errors))
            return True

        if isinstance(data, list):
            errors: List[str] = []
            for index, record in enumerate(data):
                if not isinstance(record, dict):
                    errors.append(f"record[{index}] must be a dictionary")
                    continue
                record_errors = self.validate_record(record)
                errors.extend([f"record[{index}]: {err}" for err in record_errors])
            if errors:
                raise ValueError("Record validation failed: " + "; ".join(errors))
            return True

        if hasattr(data, "columns"):
            return self._validate_dataframe(data)

        raise TypeError("Unsupported data type for validation")

    def validate_record(self, record: Dict[str, Any]) -> List[str]:
        """
        Validate a single nested record.

        Args:
            record: Dictionary representing a record

        Returns:
            List of validation error messages
        """
        errors: List[str] = []

        if not isinstance(record, dict):
            return ["Record must be a dictionary"]

        for key in self.REQUIRED_RECORD_KEYS:
            if key not in record:
                errors.append(f"Missing top-level key: '{key}'")

        if errors:
            return errors

        if not isinstance(record["user_id"], str) or not record["user_id"].strip():
            errors.append("user_id must be a non-empty string")

        platform = record["platform"]
        if not isinstance(platform, str):
            errors.append("platform must be a string")
        elif platform.lower() not in self.ALLOWED_PLATFORMS:
            errors.append(
                f"platform must be one of {sorted(self.ALLOWED_PLATFORMS)}, got '{platform}'"
            )

        cleaned_text = record["cleaned_text"]
        if not isinstance(cleaned_text, list):
            errors.append("cleaned_text must be a list of strings")
        else:
            for i, item in enumerate(cleaned_text):
                if not isinstance(item, str):
                    errors.append(f"cleaned_text[{i}] must be a string")
                elif not item.strip():
                    errors.append(f"cleaned_text[{i}] must be a non-empty string")

        timestamps = record["timestamps"]
        if not isinstance(timestamps, list):
            errors.append("timestamps must be a list")
        else:
            for i, ts in enumerate(timestamps):
                if not isinstance(ts, (int, float)):
                    errors.append(f"timestamps[{i}] must be an int or float")

        metadata = record["metadata"]
        if not isinstance(metadata, dict):
            errors.append("metadata must be a dictionary")
        else:
            for key, value in metadata.items():
                if not isinstance(value, (str, int, float, bool, type(None), dict, list)):
                    errors.append(
                        f"metadata['{key}'] contains unsupported type {type(value).__name__}"
                    )

        return errors

    def _validate_dataframe(self, df: Any) -> bool:
        """
        Validate DataFrame-like data.

        Args:
            df: DataFrame-like object

        Returns:
            True if valid, raises exception otherwise
        """
        missing_columns = set(self.required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        if len(df) < self.min_rows:
            raise ValueError(
                f"DataFrame has {len(df)} rows, minimum required: {self.min_rows}"
            )

        if self.column_types:
            for col, expected_type in self.column_types.items():
                if col in df.columns:
                    actual_type = getattr(df[col], "dtype", None)
                    if actual_type is not None and not self._type_matches(
                        actual_type, expected_type
                    ):
                        logger.warning(
                            f"Column '{col}' has type {actual_type}, expected {expected_type}"
                        )

        logger.info(f"Schema validation passed for dataframe with shape {getattr(df, 'shape', None)}")
        return True

    @staticmethod
    def _type_matches(actual_type, expected_type: str) -> bool:
        """Check if actual type matches expected type string."""
        type_mapping = {
            "int": ["int64", "int32", "int"],
            "float": ["float64", "float32", "float"],
            "str": ["object", "string"],
            "bool": ["bool"],
        }

        expected_types = type_mapping.get(expected_type, [expected_type])
        return str(actual_type) in expected_types

