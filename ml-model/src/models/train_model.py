"""
Train OCEAN personality prediction model using text (TF-IDF).
"""

import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


# Paths
DATA_PATH = "data/training/ocean_training_data.csv"
MODEL_DIR = "saved_models"

os.makedirs(MODEL_DIR, exist_ok=True)


def train_model():
    # 🔹 Load dataset
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded:", df.shape)

    # 🔹 Features and targets
    X_text = df["text"].fillna("")
    Y = df[["O", "C", "E", "A", "N"]].astype(float)

    # 🔹 TF-IDF vectorization
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(X_text)

    print("Text vectorized:", X.shape)

    # 🔹 Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42
    )

    # 🔹 Model
    model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=150,
            random_state=42,
            n_jobs=-1
        )
    )

    # 🔹 Train
    model.fit(X_train, y_train)

    print("Model training complete")

    # 🔹 Evaluate
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds, multioutput="raw_values")

    print("\nMAE for each trait:")
    print(f"O: {mae[0]:.4f}, C: {mae[1]:.4f}, E: {mae[2]:.4f}, A: {mae[3]:.4f}, N: {mae[4]:.4f}")

    # 🔹 Save model + vectorizer
    joblib.dump(model, os.path.join(MODEL_DIR, "ocean_model.pkl"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))

    print("\nModel saved in:", MODEL_DIR)


if __name__ == "__main__":
    train_model()