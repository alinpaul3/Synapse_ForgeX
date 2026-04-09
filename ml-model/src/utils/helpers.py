"""
Helper utilities.
"""

import numpy as np
import pandas as pd
from pathlib import Path


def ensure_directory(path: Path) -> Path:
    """Ensure directory exists and create if needed."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_size(path: Path) -> str:
    """Get human-readable file size."""
    size = path.stat().st_size
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    
    return f"{size:.2f} TB"


def validate_input(data, expected_type, min_length=None):
    """Validate input data."""
    if not isinstance(data, expected_type):
        raise TypeError(f"Expected {expected_type}, got {type(data)}")
    
    if min_length is not None and len(data) < min_length:
        raise ValueError(f"Data length {len(data)} is less than minimum {min_length}")
    
    return True


def scale_to_range(values: np.ndarray, min_val: float = 0, max_val: float = 1) -> np.ndarray:
    """Scale values to specified range."""
    min_v = values.min()
    max_v = values.max()
    
    if max_v == min_v:
        return np.full_like(values, (min_val + max_val) / 2, dtype=float)
    
    normalized = (values - min_v) / (max_v - min_v)
    return normalized * (max_val - min_val) + min_val
