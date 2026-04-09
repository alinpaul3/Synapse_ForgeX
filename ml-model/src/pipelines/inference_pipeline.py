"""
Inference pipeline for model predictions.
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
import pickle

logger = logging.getLogger(__name__)


class InferencePipeline:
    """Pipeline for making predictions on new data."""
    
    def __init__(
        self,
        feature_extractor,
        scaler,
        model,
        trait_names: list = None,
    ):
        """
        Initialize inference pipeline.
        
        Args:
            feature_extractor: Fitted feature extractor
            scaler: Fitted scaler
            model: Trained model
            trait_names: Names of personality traits
        """
        self.feature_extractor = feature_extractor
        self.scaler = scaler
        self.model = model
        self.trait_names = trait_names or [
            'openness', 'conscientiousness', 'extraversion', 
            'agreeableness', 'neuroticism'
        ]
    
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions and return as dataframe.
        
        Args:
            df: Input dataframe
        
        Returns:
            DataFrame with predictions
        """
        # Extract features
        X = self.feature_extractor.transform(df)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        predictions = self.model.predict(X_scaled)
        
        # Format output
        result_df = pd.DataFrame(
            predictions,
            columns=self.trait_names,
            index=df.index,
        )
        
        logger.info(f"Generated predictions for {len(df)} samples")
        return result_df
    
    def predict_batch(self, df: pd.DataFrame, batch_size: int = 32) -> pd.DataFrame:
        """
        Make batch predictions.
        
        Args:
            df: Input dataframe
            batch_size: Size of each batch
        
        Returns:
            DataFrame with predictions
        """
        results = []
        
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            batch_pred = self.predict(batch)
            results.append(batch_pred)
        
        return pd.concat(results, ignore_index=False)
    
    @classmethod
    def load(cls, directory: Path):
        """Load inference pipeline from saved files."""
        with open(directory / "feature_extractor.pkl", "rb") as f:
            feature_extractor = pickle.load(f)
        
        with open(directory / "scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        
        with open(directory / "model.pkl", "rb") as f:
            model = pickle.load(f)
        
        logger.info(f"Inference pipeline loaded from {directory}")
        return cls(feature_extractor, scaler, model)
