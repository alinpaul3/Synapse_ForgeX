"""
Training pipeline for personality detector model.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class TrainPipeline:
    """Complete training pipeline."""
    
    def __init__(
        self,
        feature_extractor,
        model_trainer,
        scaler=None,
    ):
        """
        Initialize training pipeline.
        
        Args:
            feature_extractor: Feature extraction object
            model_trainer: Model trainer object
            scaler: Optional feature scaler
        """
        self.feature_extractor = feature_extractor
        self.model_trainer = model_trainer
        self.scaler = scaler or StandardScaler()
        self.is_fitted = False
    
    def fit(self, df: pd.DataFrame, target_columns: list):
        """
        Fit the entire pipeline.
        
        Args:
            df: Input dataframe
            target_columns: Column names containing targets
        """
        # Extract features
        logger.info("Extracting features...")
        X = self.feature_extractor.fit_transform(df)
        
        # Scale features
        logger.info("Scaling features...")
        X_scaled = self.scaler.fit_transform(X)
        
        # Extract targets
        y = df[target_columns].values
        
        # Train model
        logger.info("Training model...")
        self.model_trainer.fit(X_scaled, y)
        
        self.is_fitted = True
        logger.info("Training pipeline complete")
        return self
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using the pipeline.
        
        Args:
            df: Input dataframe
        
        Returns:
            Predictions
        """
        if not self.is_fitted:
            raise RuntimeError("Pipeline must be fitted before prediction")
        
        X = self.feature_extractor.transform(df)
        X_scaled = self.scaler.transform(X)
        return self.model_trainer.predict(X_scaled)
    
    def save(self, directory: Path):
        """Save pipeline components."""
        directory.mkdir(parents=True, exist_ok=True)
        
        self.feature_extractor.save(directory / "feature_extractor.pkl")
        self.model_trainer.save(directory / "model.pkl")
        
        import pickle
        with open(directory / "scaler.pkl", "wb") as f:
            pickle.dump(self.scaler, f)
        
        logger.info(f"Pipeline saved to {directory}")
