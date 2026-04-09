"""
Text preparation and vectorization utilities.
"""

from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer


def combine_text(cleaned_text: List[str]) -> str:
    """
    Combine a list of cleaned text entries into one string.
    """
    if not cleaned_text:
        return ""
    return " ".join(str(text).strip() for text in cleaned_text if str(text).strip())


def fit_tfidf(texts: List[str], max_features: int = 5000):
    """
    Fit a TF-IDF vectorizer on a list of text documents.
    
    Returns:
        vectorizer, feature_matrix
    """
    vectorizer = TfidfVectorizer(max_features=max_features)
    X_text = vectorizer.fit_transform(texts)
    return vectorizer, X_text


def transform_tfidf(vectorizer: TfidfVectorizer, texts: List[str]):
    """
    Transform text documents using an already-fitted TF-IDF vectorizer.
    """
    return vectorizer.transform(texts)


if __name__ == "__main__":
    from src.data_loader.load_data import fetch_user_data

    request = {
        "user_id": "123"
    }

    data = fetch_user_data(request["user_id"])

    cleaned_text = data["cleaned_text"]

    combined = combine_text(cleaned_text)

    print("Combined text from REAL data:")
    print(combined)

    texts = [
        combined,
        "machine learning can predict personality traits",
        "reddit comments contain behavioral signals"
    ]

    vectorizer, X_text = fit_tfidf(texts)

    print("\nTF-IDF matrix shape:")
    print(X_text.shape)