# src/api/reservations.py
import requests
import datetime

API_BASE = "https://lotus-hms.vercel.app/frontend_api/reservations"

def get_reservations(status, date_range, search):
    params = {}
    if status and status != "All":
        params["status"] = status
    if date_range and len(date_range) == 2:
        params["arrivalDate"] = date_range[0].strftime("%Y-%m-%d")
    if search:
        if search.isdigit():
            params["confirmationNumber"] = search
        else:
            params["lastName"] = search
    try:
        resp = requests.get(API_BASE, params=params)
        resp.raise_for_status()
        data = resp.json()
        # Transform to match table columns
        result = []
        for r in data:
            result.append(r)
        return result
    except Exception as e:
        return []