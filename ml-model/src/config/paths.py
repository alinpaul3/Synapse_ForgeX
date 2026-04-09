"""
Path utilities for the personality detector project.
"""

from pathlib import Path
from .settings import (
    PROJECT_ROOT,
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    PREDICTION_OUTPUT_PATH,
    MODELS_DIR,
)


def ensure_directories_exist():
    """Ensure all required directories exist."""
    directories = [
        RAW_DATA_PATH,
        PROCESSED_DATA_PATH,
        PREDICTION_OUTPUT_PATH,
        MODELS_DIR,
        PROJECT_ROOT / "logs",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_data_file(filename: str, data_type: str = "processed") -> Path:
    """
    Get path to a data file.
    
    Args:
        filename: Name of the file
        data_type: Type of data - 'raw', 'processed', or 'output'
    
    Returns:
        Path to the data file
    """
    if data_type == "raw":
        return RAW_DATA_PATH / filename
    elif data_type == "processed":
        return PROCESSED_DATA_PATH / filename
    elif data_type == "output":
        return PREDICTION_OUTPUT_PATH / filename
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def get_model_file(model_name: str) -> Path:
    """Get path to a saved model file."""
    return MODELS_DIR / model_name
