import os
import requests
import pandas as pd
from dotenv import load_dotenv
from urllib.parse import quote_plus

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
        "country": country,
        "lang": lang
    }
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Exception fetching {app_id}:", e)
        return None

def search_appstore_app(query, country="us"):
    """Search Apple App Store for an app, returning trackId."""
    try:
        # ensure query is URL-safe
        safe_query = quote_plus(str(query))

        url = f"https://{API_HOST}/v1/app-store-api/search"
        params = {"q": safe_query, "country": country, "limit": 1}


        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        results = resp.json()

        # Some APIs return {"results": [...]}, others just a list
        if isinstance(results, dict) and "results" in results:
            results = results["results"]

        return results[0]["trackId"] if results else None

    except requests.exceptions.RequestException as e:
        print(f"Search failed for {query}:", e)
        return None
    except Exception as e:
        print(f"Unexpected error searching {query}:", e)
        return None

def merge_google_apple(google_df):
    apple_data = []
    for app in google_df['App']:
        app_id = search_appstore_app(app)
        if app_id:
            reviews = fetch_appstore_reviews(app_id)
            if reviews:
                ratings = [r.get("score", 0) for r in reviews]
                avg_rating = sum(ratings)/len(ratings) if ratings else None
                apple_data.append({
                    "App": app,
                    "AppleRating": avg_rating,
                    "AppleReviews": len(reviews)
                })
                continue
        # fallback when no match
        apple_data.append({"App": app, "AppleRating": None, "AppleReviews": 0})

    apple_df = pd.DataFrame(apple_data)
    combined = pd.merge(google_df, apple_df, on="App", how="outer")
    os.makedirs("data/cleaned_data", exist_ok=True)
    combined.to_csv("data/cleaned_data/combined_apps.csv", index=False)
    return combined
