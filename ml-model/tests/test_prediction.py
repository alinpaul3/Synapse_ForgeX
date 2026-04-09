"""
Tests for model prediction.
"""

import pytest
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

from src.models.train_model import ModelTrainer
from src.models.predict_model import Predictor


class TestModelTraining:
    """Test model training."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample training data."""
        X = np.random.randn(100, 20)
        y = np.random.randn(100, 5)
        return X, y
    
    def test_model_training(self, sample_data):
        """Test model training."""
        X, y = sample_data
        
        trainer = ModelTrainer(model_type='random_forest')
        trainer.fit(X, y)
        
        assert trainer.model is not None
    
    def test_model_prediction(self, sample_data):
        """Test model prediction."""
        X, y = sample_data
        
        trainer = ModelTrainer(model_type='random_forest')
        trainer.fit(X, y)
        
        predictions = trainer.predict(X[:10])
        assert predictions.shape == (10, 5)


class TestPredictor:
    """Test predictor."""
    
    @pytest.fixture
    def trained_model(self):
        """Create a trained model."""
        X = np.random.randn(100, 20)
        y = np.random.randn(100, 5)
        
        model = MultiOutputRegressor(RandomForestRegressor(n_estimators=10))
        model.fit(X, y)
        
        return model
    
    def test_predictor_initialization(self, trained_model):
        """Test predictor initialization."""
        predictor = Predictor(trained_model)
        assert predictor.model is not None
    
    def test_predictor_prediction(self, trained_model):
        """Test predictor prediction."""
        predictor = Predictor(trained_model)
        
        X = np.random.randn(10, 20)
        predictions = predictor.predict(X)
        
        assert predictions.shape == (10, 5)
