# src/api/reservations.py
import requests
import datetime

API_BASE = "http://localhost:8502/frontend_api/reservations"

def get_reservations(status, date_range, search):
    # params = {}
    # if status and status != "All":
    #     params["status"] = status
    # if date_range and len(date_range) == 2:
    #     params["arrivalDate"] = date_range[0].strftime("%Y-%m-%d")
    # if search:
    #     if search.isdigit():
    #         params["confirmationNumber"] = search
    #     else:
    #         params["lastName"] = search
    # try:
    #     resp = requests.get(API_BASE, params=params)
    #     resp.raise_for_status()
    #     data = resp.json()
    #     # Transform to match table columns
    #     result = []
    #     for r in data:
    #         result.append({
    #             "ReservationID": r.get("ReservationID"),
    #             "GuestName": f"{r.get('profile', {}).get('nameInfo', {}).get('FirstName', '')} {r.get('profile', {}).get('nameInfo', {}).get('LastName', '')}",
    #             "RoomNumber": r.get("reservationStay", {}).get("room", {}).get("RoomNumber", ""),
    #             "RoomType": r.get("reservationStay", {}).get("roomType", {}).get("Description", ""),
    #             "CheckIn": r.get("reservationStay", {}).get("ArrivalDate", ""),
    #             "CheckOut": r.get("reservationStay", {}).get("DepartureDate", ""),
    #             "Status": r.get("StatusCode", ""),
    #             "TotalAmount": r.get("TotalAmount", 0.0),
    #         })
    #     return result
    # except Exception as e:
    #     return []
    return [
        {
            "ID": 101,
            "ReservationID": "RES-123456",
            "GuestName": "John Doe",
            "RoomNumber": "101",
            "RoomType": "Deluxe",
            "CheckIn": "2025-05-20",
            "CheckOut": "2025-05-22",
            "Status": "confirmed",
            "TotalAmount": 200.0,
            "Property": "LOTUS Bandung",
            "Channel": "DIRECT - HOTEL WEBSITE",
            "ReservationDate": "2025-05-01",
        },
        {
            "ID": 102,
            "ReservationID": "RES-789012",
            "GuestName": "Jane Smith",
            "RoomNumber": "102",
            "RoomType": "Standard",
            "CheckIn": "2025-05-21",
            "CheckOut": "2025-05-23",
            "Status": "checked-out",
            "TotalAmount": 180.0,
            "Property": "LOTUS Bali",
            "Channel": "BOOKING.COM",
            "ReservationDate": "2025-05-02",
        },
        {
            "ID": 103,
            "ReservationID": "RES-345678",
            "GuestName": "Doe John",
            "RoomNumber": "103",
            "RoomType": "Suite",
            "CheckIn": "2025-05-22",
            "CheckOut": "2025-05-24",
            "Status": "checked-out",
            "TotalAmount": 200.0,
            "Property": "LOTUS Bandung",
            "Channel": "AGODA",
            "ReservationDate": "2025-05-03",
        },
        {
            "ID": 104,
            "ReservationID": "RES-901234",
            "GuestName": "Smith Jane",
            "RoomNumber": "104",
            "RoomType": "Standard",
            "CheckIn": "2025-05-23",
            "CheckOut": "2025-05-25",
            "Status": "confirmed",
            "TotalAmount": 200.0,
            "Property": "LOTUS Bali",
            "Channel": "EXPEDIA",
            "ReservationDate": "2025-05-04",
        },
    ]

def get_reservation_detail(reservation_id):
    try:
        resp = requests.get(f"{API_BASE}/{reservation_id}")
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

def update_reservation(reservation_id, data):
    try:
        resp = requests.patch(f"{API_BASE}/{reservation_id}", json=data)
        resp.raise_for_status()
        return True
    except Exception:
        return False

def delete_reservation(reservation_id):
    try:
        resp = requests.delete(f"{API_BASE}/{reservation_id}", json={"reason": "User deleted"})
        resp.raise_for_status()
        return True
    except Exception:
        return False
