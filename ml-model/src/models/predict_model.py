"""
Predict OCEAN personality traits using the trained model and real input data.
"""

import os
import joblib
from typing import Dict, Any

from src.features.feature_union import build_features


MODEL_PATH = "saved_models/ocean_model.pkl"
VECTORIZER_PATH = "saved_models/tfidf_vectorizer.pkl"


def predict_ocean_from_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict OCEAN scores from one real input record.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(f"Vectorizer not found: {VECTORIZER_PATH}")

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    features = build_features(record)
    text = features["text"]

    X = vectorizer.transform([text])
    pred = model.predict(X)[0]

    return {
        "user_id": record["user_id"],
        "platform": record["platform"],
        "O": round(float(pred[0]), 4),
        "C": round(float(pred[1]), 4),
        "E": round(float(pred[2]), 4),
        "A": round(float(pred[3]), 4),
        "N": round(float(pred[4]), 4),
    }


if __name__ == "__main__":
    from src.data_loader.load_data import fetch_user_data

    request = {
        "user_id": "123"
    }

    data = fetch_user_data(request["user_id"])
    result = predict_ocean_from_record(data)

    print("Predicted OCEAN scores:")
    print(result)