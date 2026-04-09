"""
Batch scoring pipeline for processing multiple predictions.
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class BatchScoringPipeline:
    """Process batch predictions and export results."""
    
    def __init__(self, inference_pipeline):
        """
        Initialize batch scoring pipeline.
        
        Args:
            inference_pipeline: Fitted inference pipeline
        """
        self.pipeline = inference_pipeline
    
    def score_batch(self, input_data: pd.DataFrame) -> pd.DataFrame:
        """
        Score a batch of data.
        
        Args:
            input_data: Input dataframe
        
        Returns:
            DataFrame with personality scores
        """
        logger.info(f"Scoring batch of {len(input_data)} samples")
        
        predictions = self.pipeline.predict(input_data)
        
        # Normalize scores to 0-100 scale
        predictions = predictions.clip(0, 1) * 100
        
        return predictions
    
    def process_and_export(
        self,
        input_data: pd.DataFrame,
        output_path: Path,
        format: str = 'csv',
    ) -> Path:
        """
        Process batch and export results.
        
        Args:
            input_data: Input dataframe
            output_path: Path to save results
            format: Output format ('csv', 'json', 'excel')
        
        Returns:
            Path to saved file
        """
        # Score the batch
        predictions = self.score_batch(input_data)
        
        # Add original data
        result_df = pd.concat([input_data, predictions], axis=1)
        
        # Save results
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'csv':
            result_df.to_csv(output_path, index=False)
        elif format == 'json':
            result_df.to_json(output_path, orient='records')
        elif format == 'excel':
            result_df.to_excel(output_path, index=False)
        
        logger.info(f"Results exported to {output_path}")
        return output_path
