"""
Configuration settings for the personality detector ML model.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "saved_models"

# Data paths
RAW_DATA_PATH = DATA_DIR / "raw_exports"
PROCESSED_DATA_PATH = DATA_DIR / "processed_input"
PREDICTION_OUTPUT_PATH = DATA_DIR / "prediction_output"

# Model paths
VECTORIZER_PATH = MODELS_DIR / "vectorizer.pkl"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
OCEAN_MODEL_PATH = MODELS_DIR / "ocean_model.pkl"
FUSION_MODEL_PATH = MODELS_DIR / "fusion_model.pkl"

# Model parameters
OCEAN_TRAITS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
TEST_SIZE = 0.2
RANDOM_STATE = 42
BATCH_SIZE = 32

# Feature engineering
MAX_TEXT_LENGTH = 5000
MIN_TEXT_LENGTH = 10
N_TEXT_FEATURES = 100

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = PROJECT_ROOT / "logs" / "ml_model.log"

# API configuration
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", 5000))
