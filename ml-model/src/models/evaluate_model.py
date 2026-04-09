"""
Model evaluation utilities.
"""

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluate model performance."""
    
    @staticmethod
    def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
        """
        Evaluate predictions against ground truth.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
        
        Returns:
            Dictionary of metrics
        """
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        
        metrics = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2_score': r2,
        }
        
        logger.info(f"Evaluation metrics: {metrics}")
        return metrics
    
    @staticmethod
    def evaluate_per_output(y_true: np.ndarray, y_pred: np.ndarray, output_names=None) -> dict:
        """
        Evaluate multi-output model per output.
        
        Args:
            y_true: True labels (n_samples, n_outputs)
            y_pred: Predicted labels (n_samples, n_outputs)
            output_names: Names of outputs
        
        Returns:
            Dictionary with metrics per output
        """
        n_outputs = y_true.shape[1] if y_true.ndim > 1 else 1
        results = {}
        
        for i in range(n_outputs):
            if y_true.ndim > 1:
                y_t, y_p = y_true[:, i], y_pred[:, i]
                name = output_names[i] if output_names else f"output_{i}"
            else:
                y_t, y_p = y_true, y_pred
                name = output_names[0] if output_names else "output_0"
            
            results[name] = ModelEvaluator.evaluate(y_t, y_p)
        
        return results
