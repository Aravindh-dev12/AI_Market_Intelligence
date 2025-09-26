import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

BASE_URL = f"https://{API_HOST}/v1/app-store-api/reviews"

# Example apps with known Apple App IDs
APPLE_APP_IDS = {
    "Photo Editor & Candy Camera & Grid & ScrapBook": 364709193,
    "Coloring book moana": 123456789,
    "U Launcher Lite – FREE Live Cool Themes, Hide Apps": 987654321,
    # add more as needed
}

def fetch_reviews(app_id, page=1, country="us", lang="en", retries=3):
    params = {
        "id": app_id,
        "sort": "mostRecent",
        "page": page,
        "country": country,  # fixed typo from 'contry'
        "lang": lang
    }

    for attempt in range(1, retries+1):
        try:
            resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            status = resp.status_code if 'resp' in locals() else 'unknown'
            print(f"HTTPError (status {status}) on attempt {attempt} for app_id {app_id}: {e}")
            if status == 429:  # rate limit
                wait = 2 ** attempt
                print(f"Rate limited. Waiting {wait}s before retry...")
                time.sleep(wait)
            elif status == 403:
                print("Forbidden. Skipping this app.")
                return None
            else:
                time.sleep(1)
        except Exception as e:
            print(f"Error fetching app_id {app_id}:", e)
            time.sleep(1)
    return None

def merge_google_apple(google_df):
    apple_data = []
    for app in google_df['App']:
        app_id = APPLE_APP_IDS.get(app)
        if not app_id:
            print(f"No Apple App ID for {app}. Skipping.")
            apple_data.append({"App": app, "AppleRating": None, "AppleReviews": 0})
            continue

        reviews = fetch_reviews(app_id)
        if reviews:
            ratings = [r.get("score", 0) for r in reviews]
            avg_rating = sum(ratings)/len(ratings) if ratings else None
            apple_data.append({
                "App": app,
                "AppleRating": avg_rating,
                "AppleReviews": len(reviews)
            })
        else:
            apple_data.append({"App": app, "AppleRating": None, "AppleReviews": 0})

    apple_df = pd.DataFrame(apple_data)
    combined = pd.merge(google_df, apple_df, on="App", how="outer")
    os.makedirs("data/cleaned_data", exist_ok=True)
    combined.to_csv("data/cleaned_data/combined_apps.csv", index=False)
    print("✅ Combined data saved to data/cleaned_data/combined_apps.csv")
    return combined

def main():
    # Example Google Play data
    google_data = {"App": list(APPLE_APP_IDS.keys())}
    google_df = pd.DataFrame(google_data)

    print("Merging with Apple App Store data...")
    combined_df = merge_google_apple(google_df)
    print(combined_df)

if __name__ == "__main__":
    main()
