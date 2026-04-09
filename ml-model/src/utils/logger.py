"""
Logging configuration.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from src.config.settings import LOG_LEVEL, LOG_FILE


def setup_logging(name: str = None) -> logging.Logger:
    """
    Configure logging.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Create logs directory
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5,
    )
    file_handler.setLevel(LOG_LEVEL)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger
