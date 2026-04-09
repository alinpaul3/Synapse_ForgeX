"""
Tests for feature extraction.
"""

import pytest
import pandas as pd
import numpy as np

from src.features.text_vectorizer import TextVectorizer
from src.features.metadata_features import MetadataFeatures


class TestTextVectorizer:
    """Test text vectorization."""
    
    @pytest.fixture
    def sample_texts(self):
        """Create sample texts."""
        return [
            "I love this product, it works great",
            "This is terrible, I hate it",
            "Amazing quality and great service",
            "Not satisfied with my purchase",
            "Best decision I ever made",
        ]
    
    def test_vectorizer_fit(self, sample_texts):
        """Test vectorizer fitting."""
        vectorizer = TextVectorizer(max_features=10)
        vectorizer.fit(sample_texts)
        assert vectorizer.is_fitted
    
    def test_vectorizer_transform(self, sample_texts):
        """Test vectorizer transform."""
        vectorizer = TextVectorizer(max_features=10)
        vectors = vectorizer.fit_transform(sample_texts)
        
        assert vectors.shape[0] == len(sample_texts)
        assert vectors.shape[1] <= 10
    
    def test_vectorizer_transform_before_fit_raises_error(self, sample_texts):
        """Test transform before fit raises error."""
        vectorizer = TextVectorizer()
        with pytest.raises(RuntimeError):
            vectorizer.transform(sample_texts)


class TestMetadataFeatures:
    """Test metadata feature extraction."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data."""
        return pd.DataFrame({
            'text': [
                'hello world',
                'this is a longer text example',
                'short',
            ],
            'age': [25, 35, 45],
            'gender': ['M', 'F', 'M'],
        })
    
    def test_metadata_extraction(self, sample_data):
        """Test metadata feature extraction."""
        features = MetadataFeatures.extract(sample_data)
        
        assert 'word_count' in features.columns
        assert 'char_count' in features.columns
        assert len(features) == len(sample_data)
