from fastapi import FastAPI
from pydantic import BaseModel

from src.data_loader.load_data import fetch_user_data
from src.models.predict_model import predict_ocean_from_record
from src.api_payload.format_scores import format_scores

app = FastAPI()


class PredictionRequest(BaseModel):
    user_id: str


@app.post("/predict")
def predict(request: PredictionRequest):
    data = fetch_user_data(request.user_id)
    prediction = predict_ocean_from_record(data)
    return format_scores(prediction)