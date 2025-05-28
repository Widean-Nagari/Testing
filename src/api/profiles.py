# src/api/reservations.py
import requests
import datetime

API_BASE = "https://lotus-hms.vercel.app/frontend_api/profiles"

def get_user_profiles():
    """Fetch user profiles from the API."""
    try:
        resp = requests.get(API_BASE)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
