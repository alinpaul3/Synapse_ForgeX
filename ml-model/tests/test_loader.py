"""
Tests for data loading functionality.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile

from src.data_loader.load_data import load_data, save_data


class TestDataLoader:
    """Test data loading utilities."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'id': range(10),
            'text': ['sample text'] * 10,
            'label': np.random.rand(10),
        })
    
    def test_save_and_load_csv(self, sample_data):
        """Test saving and loading CSV files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.csv"
            
            # Save
            save_data(sample_data, path)
            assert path.exists()
            
            # Load
            loaded_data = load_data(path)
            assert len(loaded_data) == len(sample_data)
            assert list(loaded_data.columns) == list(sample_data.columns)
    
    def test_save_and_load_json(self, sample_data):
        """Test saving and loading JSON files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.json"
            
            # Save
            save_data(sample_data, path)
            assert path.exists()
            
            # Load
            loaded_data = load_data(path)
            assert len(loaded_data) == len(sample_data)
    
    def test_load_nonexistent_file(self):
        """Test loading nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            load_data(Path("nonexistent.csv"))
