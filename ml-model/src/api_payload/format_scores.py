"""
Format model predictions into API / n8n friendly JSON.
"""

from typing import Dict, Any


def format_scores(prediction: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "user_id": prediction["user_id"],
        "platform": prediction["platform"],
        "O": prediction["O"],
        "C": prediction["C"],
        "E": prediction["E"],
        "A": prediction["A"],
        "N": prediction["N"],
    }