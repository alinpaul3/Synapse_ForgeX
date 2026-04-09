"""
OCEAN personality model.
Predicts Big Five personality traits (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism).
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)


class OCEANRegressor:
    """Predicts OCEAN personality traits."""
    
    TRAITS = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    TRAIT_DESCRIPTIONS = {
        'openness': 'Openness to Experience',
        'conscientiousness': 'Conscientiousness',
        'extraversion': 'Extraversion',
        'agreeableness': 'Agreeableness',
        'neuroticism': 'Neuroticism',
    }
    
    def __init__(self, base_regressor):
        """
        Initialize OCEAN regressor.
        
        Args:
            base_regressor: Base regression model (must support multi-output)
        """
        self.regressor = base_regressor
        self.trait_scaling = {trait: {'min': 0, 'max': 100} for trait in self.TRAITS}
    
    def fit(self, X, y):
        """
        Fit the model on training data.
        
        Args:
            X: Feature matrix
            y: Target matrix with 5 personality trait columns
        """
        self.regressor.fit(X, y)
        logger.info(f"OCEAN regressor fitted with {X.shape[0]} samples")
        return self
    
    def predict(self, X, normalize: bool = True) -> dict:
        """
        Predict OCEAN traits.
        
        Args:
            X: Feature matrix
            normalize: Whether to normalize scores to 0-100 range
        
        Returns:
            Dictionary mapping trait names to prediction arrays
        """
        predictions = self.regressor.predict(X)
        
        if normalize:
            predictions = np.clip(predictions, 0, 1) * 100
        
        results = {}
        for i, trait in enumerate(self.TRAITS):
            results[trait] = predictions[:, i]
        
        return results
    
    def predict_single(self, X) -> dict:
        """
        Predict for a single sample and return as dict.
        
        Args:
            X: Single sample (1D array or 2D with 1 row)
        
        Returns:
            Dictionary with trait names and values
        """
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        predictions = self.predict(X)
        return {trait: float(values[0]) for trait, values in predictions.items()}
