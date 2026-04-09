import requests
import logging

# Set up logger
logger = logging.getLogger(__name__)

BASE_URL = "https://archetypal-anthropographic-hana.ngrok-free.dev"

def fetch_user_data(user_id: str) -> dict:
    """
    Fetch processed user data from backend API.
    """
    url = f"{BASE_URL}/processed-data/{user_id}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        data = response.json()
        logger.info(f"Fetched data for user {user_id}")
        return data

    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        raise