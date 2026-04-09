# Personality Detector ML Model

A machine learning model for detecting and predicting personality traits (OCEAN model) from text and metadata.

## Project Structure

```
ml-model/
├── data/                          # Data directory
│   ├── raw_exports/              # Raw exported data
│   ├── processed_input/          # Processed input data
│   └── prediction_output/        # Model prediction outputs
│
├── notebooks/                     # Jupyter notebooks
│   ├── 01_eda.ipynb              # Exploratory data analysis
│   ├── 02_feature_checks.ipynb   # Feature engineering checks
│   └── 03_model_experiments.ipynb # Model experimentation
│
├── src/                           # Source code
│   ├── config/                   # Configuration files
│   ├── data_loader/              # Data loading utilities
│   ├── features/                 # Feature engineering
│   ├── models/                   # Model implementations
│   ├── pipelines/                # ML pipelines
│   ├── utils/                    # Utility functions
│   └── api_payload/              # API response formatting
│
├── tests/                         # Unit tests
│   ├── test_loader.py
│   ├── test_features.py
│   └── test_prediction.py
│
├── saved_models/                 # Serialized models
│
└── README.md                     # This file
```

## Features

- **Text Vectorization**: TF-IDF based text feature extraction
- **Metadata Features**: Age, gender, and linguistic features
- **Platform Features**: Social media platform encoding
- **Time Features**: Temporal patterns (hour, day of week, etc.)
- **OCEAN Model**: Big Five personality trait prediction (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- **Fusion Model**: Ensemble predictions from multiple models
- **API Integration**: Format predictions for API responses and n8n workflows

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run Main Script
```bash
python main.py
```

### Jupyter Notebooks
```bash
jupyter notebook notebooks/
```

### Run Tests
```bash
pytest tests/ -v
```

### Import in Your Code
```python
from src.models.train_model import ModelTrainer
from src.features.text_vectorizer import TextVectorizer
from src.pipelines.inference_pipeline import InferencePipeline

# Load and preprocess data
# Create features
# Train model
# Make predictions
```

## Model Pipeline

### Training Pipeline
1. Load raw data
2. Extract features (text, metadata, platform, time)
3. Scale features (StandardScaler)
4. Train multi-output regression model
5. Save model, scaler, and feature extractor

### Inference Pipeline
1. Load trained model, scaler, and feature extractor
2. Process input data
3. Extract features
4. Make predictions
5. Format output

## Configuration

Edit `src/config/settings.py` to customize:
- Data paths
- Model hyperparameters
- Feature parameters
- Logging configuration

Set environment variables in `.env`:
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `API_HOST`: API host address
- `API_PORT`: API port number

## API Response Format

Personality scores are returned in 0-100 scale:
```json
{
  "personality": {
    "openness": {
      "score": 75.5,
      "percentile": 75,
      "interpretation": "High"
    },
    "conscientiousness": {...},
    ...
  },
  "summary": {
    "dominant_trait": "openness",
    "dominant_score": 75.5,
    "overall_stability": 68.2
  }
}
```

## n8n Integration

Export predictions for n8n workflows:
```python
from src.api_payload.export_for_n8n import N8nExporter

# Export to JSON
N8nExporter.export_json(predictions_df, output_path)

# Create webhook payload
payload = N8nExporter.export_webhook_payload(predictions_df, webhook_url)
```

## Testing

Run test suite:
```bash
pytest tests/ -v --cov=src
```

## License

Proprietary - All rights reserved

## Author

Personality Detector Team
