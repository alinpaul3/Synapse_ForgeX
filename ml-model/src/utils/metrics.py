"""
Metrics and evaluation utilities.
"""

import numpy as np
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error,
)


class Metrics:
    """Collection of evaluation metrics."""
    
    @staticmethod
    def mse(y_true, y_pred):
        """Mean Squared Error."""
        return mean_squared_error(y_true, y_pred)
    
    @staticmethod
    def rmse(y_true, y_pred):
        """Root Mean Squared Error."""
        return np.sqrt(mean_squared_error(y_true, y_pred))
    
    @staticmethod
    def mae(y_true, y_pred):
        """Mean Absolute Error."""
        return mean_absolute_error(y_true, y_pred)
    
    @staticmethod
    def mape(y_true, y_pred):
        """Mean Absolute Percentage Error."""
        return mean_absolute_percentage_error(y_true, y_pred)
    
    @staticmethod
    def r2(y_true, y_pred):
        """R-squared Score."""
        return r2_score(y_true, y_pred)
    
    @staticmethod
    def compute_all(y_true, y_pred) -> dict:
        """Compute all metrics."""
        return {
            'mse': Metrics.mse(y_true, y_pred),
            'rmse': Metrics.rmse(y_true, y_pred),
            'mae': Metrics.mae(y_true, y_pred),
            'mape': Metrics.mape(y_true, y_pred),
            'r2': Metrics.r2(y_true, y_pred),
        }
