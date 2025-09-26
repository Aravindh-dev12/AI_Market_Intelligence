import os
import requests
import pandas as pd
from dotenv import load_dotenv
from time import sleep

load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

BASE_URL = f"https://{API_HOST}/v1/app-store-api/reviews"

def fetch_appstore_reviews(app_id, page=1, country="us", lang="en"):
    params = {
        "id": app_id,
        "sort": "mostRecent",
        "page": page,
        "contry": country,   
        "lang": lang
    }
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Exception fetching {app_id}:", e)
        return None
def merge_google_apple(google_df):
    apple_data = []
    example_app_ids = [364709193, 123456789, 987654321]

    for i, app in enumerate(google_df['App'].head(len(example_app_ids))):
        app_id = example_app_ids[i]
        reviews = fetch_appstore_reviews(app_id)
        if reviews:
            ratings = [r.get("score", 0) for r in reviews]  
            avg_rating = sum(ratings)/len(ratings) if ratings else None
            apple_data.append({
                "App": app,
                "AppleRating": avg_rating,
                "AppleReviews": len(reviews)
            })
        else:
            apple_data.append({
                "App": app,
                "AppleRating": None,
                "AppleReviews": 0
            })
    apple_df = pd.DataFrame(apple_data)
    combined = pd.merge(google_df, apple_df, on="App", how="outer")
    combined.to_csv("data/cleaned_data/combined_apps.csv", index=False)
    return combined
