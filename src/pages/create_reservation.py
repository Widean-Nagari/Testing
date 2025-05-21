# src/pages/create_reservation.py
import streamlit as st
import pandas as pd
from api.reservations import get_reservation_detail, update_reservation, delete_reservation

def main():
    st.set_page_config(page_title="Hotel Reservation Admin Dashboard", layout="wide")
    st.title("Create Reservation")

    # Guest Information Section
    st.subheader("Guest Information")
    if "show_guest_form" not in st.session_state:
        st.session_state["show_guest_form"] = False

    if not st.session_state["show_guest_form"]:
        search_query = st.text_input("Search Guest by Name or Email")
        if st.button("Create New Guest Profile", key="create_guest_profile"):
            st.session_state["show_guest_form"] = True
    else:
        with st.form("guest_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name")
                email = st.text_input("Email Address")
            with col2:
                last_name = st.text_input("Last Name")
                phone = st.text_input("Phone Number")
            
            address = st.text_input("Address")
            col1, col2 = st.columns(2)
            with col1:
                city = st.text_input("City")
                postal_code = st.text_input("Postal Code")
            with col2:
                state = st.text_input("State/Province")
                country = st.text_input("Country")
            guest_form_submitted = st.form_submit_button("Save Guest Profile")
            if guest_form_submitted:
                st.success("Guest profile saved (dummy, not saved).")
        if st.button("Cancel", key="cancel_guest_form"):
            st.session_state["show_guest_form"] = False

    # Stay Information Section
    st.subheader("Stay Information")
    col1, col2 = st.columns(2)
    with col1:
        arrival_date = st.date_input("Arrival Date")
        
        # Update room type dropdown to use name-value pairs and add a default option
        room_types = [
            {"name": "Select Room Type", "value": None},
            {"name": "Standard Room (Rp. 2.000.000)", "value": 2000000},
            {"name": "Deluxe Room (Rp. 3.500.000)", "value": 3500000},
            {"name": "Suite (Rp. 5.500.000)", "value": 5500000},
            {"name": "Standard Room (Rp. 1.500.000)", "value": 1500000},
            {"name": "Deluxe Room (Rp. 2.500.000)", "value": 2500000},
            {"name": "Suite (Rp. 400.000)", "value": 400000}
        ]

        room_type_selection = st.selectbox("Room Type", [room["name"] for room in room_types])
        selected_room_value = next((room["value"] for room in room_types if room["name"] == room_type_selection), None)

        # Update rate based on selected room type
        rate = st.number_input("Rate (per night) in IDR", value=selected_room_value if selected_room_value else 0)

        adults = st.number_input("Number of Adults", min_value=1, step=1)
    with col2:
        departure_date = st.date_input("Departure Date")
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
        specific_room = st.selectbox(
            "Select Specific Room",
            ["Room 101", "Room 102", "Room 103"] if selected_room_value else [],
            disabled=not selected_room_value
        )
        if not selected_room_value:
            st.text("Please select a room type first")

        col1, col2 = st.columns(2)
        with col1:
            id_type = st.selectbox("ID Type", ["Passport", "Driver License", "ID Card"])
        with col2:
            id_number = st.text_input("ID Number")
    notes = st.text_area("Notes")

    # Action Buttons
    if st.button("Cancel", key="cancel_reservation"):
        st.info("Reservation creation cancelled.")
    if st.button("Create & Check In", key="create_reservation"):
        st.success("Reservation created (dummy, not saved).")

main()