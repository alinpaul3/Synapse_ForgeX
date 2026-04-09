from src.data_loader.load_data import fetch_user_data
from src.models.predict_model import predict_ocean_from_record
from src.api_payload.format_scores import format_scores


def run_pipeline(user_id: str):
    data = fetch_user_data(user_id)
    prediction = predict_ocean_from_record(data)
    formatted = format_scores(prediction)
    return formatted


if __name__ == "__main__":
    user_id = "123"
    output = run_pipeline(user_id)
    print(output)
