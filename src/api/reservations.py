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

def get_reservation_detail(reservation_id):
    try:
        resp = requests.get(f"{API_BASE}/{reservation_id}")
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

def create_reservation(data):
    """Create a new reservation."""
    try:
        resp = requests.post(API_BASE, json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def update_reservation(reservation_id, data):
    """Update reservation notes or stay details."""
    try:
        resp = requests.patch(f"{API_BASE}/{reservation_id}", json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def delete_reservation(reservation_id, reason):
    """Cancel a reservation."""
    try:
        resp = requests.delete(f"{API_BASE}/{reservation_id}", json={"reason": reason})
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def check_in(reservation_id, data):
    """Check-in a guest."""
    try:
        resp = requests.post(f"{API_BASE}/{reservation_id}/check-in", json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def check_out(reservation_id):
    """Check-out a guest."""
    try:
        resp = requests.post(f"{API_BASE}/{reservation_id}/check-out")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def transform_reservations(data):
    """Transform reservations for optimized storage/transmission."""
    try:
        resp = requests.post(f"{API_BASE}/transform", json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def optimize_reservations(data):
    """Optimize reservations for storage/transmission."""
    try:
        resp = requests.post(f"{API_BASE}/optimize", json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
