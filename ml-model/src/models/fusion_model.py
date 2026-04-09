"""
Fusion model combining ensemble predictions.
"""

import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class FusionModel:
    """Ensemble fusion model for personality prediction."""
    
    def __init__(self, models: list, weights: list = None):
        """
        Initialize fusion model.
        
        Args:
            models: List of trained models
            weights: Weights for each model (default: equal weights)
        """
        self.models = models
        
        if weights is None:
            weights = [1.0 / len(models)] * len(models)
        else:
            total = sum(weights)
            weights = [w / total for w in weights]
        
        self.weights = weights
        logger.info(f"Fusion model initialized with {len(models)} models")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make ensemble predictions.
        
        Args:
            X: Feature matrix
        
        Returns:
            Weighted ensemble predictions
        """
        predictions = []
        
        for model, weight in zip(self.models, self.weights):
            pred = model.predict(X)
            predictions.append(pred * weight)
        
        ensemble_pred = np.sum(predictions, axis=0)
        logger.info(f"Made ensemble predictions for {len(X)} samples")
        return ensemble_pred
    
    def predict_with_variance(self, X: np.ndarray) -> tuple:
        """
        Make predictions with uncertainty estimates.
        
        Args:
            X: Feature matrix
        
        Returns:
            Tuple of (ensemble_predictions, variance)
        """
        predictions = []
        
        for model in self.models:
            pred = model.predict(X)
            predictions.append(pred)
        
        predictions = np.array(predictions)
        ensemble_pred = np.average(predictions, axis=0, weights=self.weights)
        variance = np.var(predictions, axis=0)
        
        return ensemble_pred, variance
