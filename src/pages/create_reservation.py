# src/pages/create_reservation.py
import streamlit as st
import pandas as pd
import random
from api.reservations import get_reservations, get_reservation_detail, update_reservation, delete_reservation, create_reservation, check_in
from api.profiles import get_user_profiles

def main():
    st.set_page_config(page_title="Hotel Reservation Admin Dashboard", layout="wide")
    st.title("Create Reservation")

    all_reservations = get_reservations(None, None, None)  # Fetch all reservations initially

    # Guest Information Section
    st.subheader("Guest Information")
    if "show_guest_form" not in st.session_state:
        st.session_state["show_guest_form"] = False


    guest_profiles = get_user_profiles()
    if not st.session_state["show_guest_form"]:
        if "error" in guest_profiles:
            st.error("Failed to fetch guest profiles.")
            guest_profiles = []
        else:
            guest_profiles = guest_profiles if isinstance(guest_profiles, list) else []

        guest_profile_selection = st.selectbox(
            "Select Guest Profile",
            [f"{profile['FirstName']} {profile['LastName']} ({profile['EmailAddress']})" for profile in guest_profiles]
        )
        selected_guest_profile = next((profile for profile in guest_profiles if f"{profile['FirstName']} {profile['LastName']} ({profile['EmailAddress']})" == guest_profile_selection), None)
        
        st.session_state["selected_guest_profile"] = selected_guest_profile

        if st.button("Create New Guest Profile", key="create_guest_profile"):
            st.session_state["show_guest_form"] = True
    else:
        st.session_state["selected_guest_profile"]["ProfileID"] = len(guest_profiles) + 1
        col1, col2 = st.columns(2)
        with col1:
            st.text_input(
                "First Name",
                key="FirstName",
                on_change=lambda: st.session_state["selected_guest_profile"].update({"FirstName": st.session_state["FirstName"]}),
            )
            st.text_input(
                "Email Address",
                key="EmailAddress",
                on_change=lambda: st.session_state["selected_guest_profile"].update({"EmailAddress": st.session_state["EmailAddress"]}),
            )
        with col2:
            st.text_input(
                "Last Name",
                key="LastName",
                on_change=lambda: st.session_state["selected_guest_profile"].update({"LastName": st.session_state["LastName"]}),
            )
            st.text_input(
                "Phone Number",
                key="PhoneNumber",
                on_change=lambda: st.session_state["selected_guest_profile"].update({"PhoneNumber": st.session_state["PhoneNumber"]}),
            )

        st.text_input(
            "Address",
            key="Address",
            on_change=lambda: st.session_state["selected_guest_profile"].update({"Address": st.session_state["Address"]}),
        )
        col1, col2 = st.columns(2)
        with col1:
            st.text_input(
                "City",
                key="City",
                on_change=lambda: st.session_state["selected_guest_profile"].update({"City": st.session_state["City"]}),
            )
            st.text_input(
                "Postal Code",
                key="PostalCode",
                on_change=lambda: st.session_state["selected_guest_profile"].update({"PostalCode": st.session_state["PostalCode"]}),
            )
        with col2:
            st.text_input(
                "State/Province",
                key="State",
                on_change=lambda: st.session_state["selected_guest_profile"].update({"State": st.session_state["State"]}),
            )
            st.text_input(
                "Country",
                key="Country",
                on_change=lambda: st.session_state["selected_guest_profile"].update({"Country": st.session_state["Country"]}),
            )
        if st.button("Cancel", key="cancel_guest_form"):
            st.session_state["show_guest_form"] = False

    # Stay Information Section
    st.subheader("Stay Information")
    col1, col2 = st.columns(2)
    with col1:
        arrival_date = st.date_input("Arrival Date")
        
        # Update room type dropdown to use name-value pairs and add a default option
        room_types = [
            {"id": 1, "name": "Select Room Type", "price": None},
            {"id": 2, "name": "Standard Room (Rp. 2.000.000)", "price": 2000000},
            {"id": 3, "name": "Deluxe Room (Rp. 3.500.000)", "price": 3500000},
            {"id": 4, "name": "Suite (Rp. 5.500.000)", "price": 5500000},
            {"id": 5, "name": "Standard Room (Rp. 1.500.000)", "price": 1500000},
            {"id": 6, "name": "Deluxe Room (Rp. 2.500.000)", "price": 2500000},
            {"id": 7, "name": "Suite (Rp. 400.000)", "price": 400000}
        ]

        room_type_selection = st.selectbox("Room Type", [room["name"] for room in room_types])
        selected_room = next((room for room in room_types if room["name"] == room_type_selection), None)
        selected_room_type_id = selected_room["id"] if selected_room else None
        adults = st.number_input("Number of Adults", min_value=1, step=1)
    with col2:
        departure_date = st.date_input("Departure Date")
        rate = st.number_input("Rate (per night) in IDR", value=selected_room["price"] if selected_room else 0)
        children = st.number_input("Number of Children", min_value=0, step=1)

    # Booking Information Section
    st.subheader("Booking Information")
    booking_channel = st.selectbox("Booking Channel", [
        "Direct - Hotel Website",
        "Direct - Phone",
        "Direct - Walk in",
        "Booking.com",
        "Expedia",
        "Airbnb",
        "Agoda",
        "Other OTA"
    ])
    immediate_checkin = st.checkbox("Guest is present for immediate check-in")
    if immediate_checkin:
        # Update specific room dropdown to use id-name pairs
        specific_rooms = [
            {"id": 1, "name": "Room 101"},
            {"id": 2, "name": "Room 102"},
            {"id": 3, "name": "Room 103"}
        ] if selected_room else []

        specific_room_selection = st.selectbox(
            "Select Specific Room",
            [room["name"] for room in specific_rooms],
            disabled=not selected_room
        )
        selected_specific_room = next((room for room in specific_rooms if room["name"] == specific_room_selection), None)
        specific_room_id = selected_specific_room["id"] if selected_specific_room else None

        col1, col2 = st.columns(2)
        with col1:
            id_type = st.selectbox("ID Type", ["Passport", "Driver License", "ID Card"])
        with col2:
            id_number = st.text_input("ID Number")
    notes = st.text_area("Notes")

    # Action Buttons
    st.markdown("""
        <style>
            .cancel-button {
                text-decoration: none !important;
                color: white !important;
                padding: 10px 15px;
                border-radius: 10px;
                border: 1px solid #41444c;
            }
            .cancel-button:hover {
                color: red !important;
                border-color: red;
            }
        </style>
        <a href="/reservation_list" target="_self" class="cancel-button">Cancel</a>
    """, unsafe_allow_html=True)
    if st.button("Create & Check In", key="create_reservation"):
        random_digits = ''.join(random.choices('0123456789', k=6))
        profile = st.session_state.get("selected_guest_profile")
        reservation_data = {
            "ConfirmationNumber": "RES"+random_digits,
            "StatusCode": 'confirmed',
            "ProfileID": profile.get("ProfileID", 1),
            "profile": {
                "FirstName": profile["FirstName"],
                "LastName": profile["LastName"],
                "EmailAddress": profile["EmailAddress"],
                "PhoneNumber": profile["PhoneNumber"],
            },
            "reservationStays": [
                {
                    "ArrivalDate": arrival_date.strftime("%Y-%m-%d"),
                    "DepartureDate": departure_date.strftime("%Y-%m-%d"),
                    "RoomTypeID": selected_room_type_id,
                    "RoomID": specific_room_id if immediate_checkin else None
                }
            ],
            "BookingChannelCode": booking_channel.upper(),
            "PropertyID": 1  # Example property ID, replace with actual logic
        }

        response = create_reservation(reservation_data)
        if "error" in response:
            st.error(f"Failed to create reservation: {response['error']}")
        else:
            if immediate_checkin:
                check_in_data = {
                    "roomId": specific_room_id,
                    "guestDetails": {
                        "useReservedGuest": True,
                        "guests": [
                            {
                                "firstName": profile["FirstName"],
                                "lastName": profile["LastName"],
                                "idType": id_type,
                                "idNumber": id_number,
                                "isPrimary": True
                            }
                        ]
                    },
                    "paymentMethod": "Credit Card",  # Example payment method
                    "specialRequests": notes
                }

                check_in_response = check_in(response["ReservationID"], check_in_data)
                if "error" in check_in_response:
                    st.error(f"Failed to check in: {check_in_response['error']}")
                else:
                    st.success(f"Reservation created successfully with ID: {response['ReservationID']}")

main()