import streamlit as st
import pandas as pd
from datetime import datetime
from api.reservations import update_reservation, get_reservation_detail

def main():
    st.set_page_config(page_title="Update Reservation", layout="wide")
    st.title("Update Reservation")

    # Get reservation ID from query params
    reservation_id = st.query_params.get("id", [None])[0]
    if not reservation_id:
        st.error("Reservation ID is missing.")
        return

    # Fetch reservation details
    reservation_details = get_reservation_detail(reservation_id)
    if not reservation_details:
        st.error("Failed to fetch reservation details.")
        return

    name = reservation_details['ProfileNamePrefix'] + ' ' + reservation_details['ProfileFirstName'] + ' ' + reservation_details['ProfileLastName']
    st.subheader(name)
    
    # Pre-fill fields with reservation details
    check_in_date = st.date_input("Check-in Date", value=pd.to_datetime(reservation_details['reservationStays'][0]['ArrivalDate']))
    check_out_date = st.date_input("Check-out Date", value=pd.to_datetime(reservation_details['reservationStays'][0]['DepartureDate']))
    number_of_adults = st.number_input("Number of Adults", min_value=1, step=1, value=reservation_details['reservationStays'][0].get('AdultCount', 1))
    number_of_children = st.number_input("Number of Children", min_value=0, step=1, value=reservation_details['reservationStays'][0].get('ChildCount', 0))
    
    col1, col2 = st.columns(2)
    with col1:
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
    with col2:
        # Update rate based on selected room type
        rate_amount = st.number_input("Rate (per night) in IDR", value=selected_room_value if selected_room_value else 0)
        # rate_amount = st.number_input("Rate Amount", min_value=0.0, step=0.01, value=float(reservation_details['reservationStays'][0]['RateAmount']))

    notes = st.text_area("Notes", value=reservation_details.get('notes', ''))

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

    if st.button("Save Changes"):
        update_data = {
            "stays": [
                {
                    "ReservationStayID": reservation_details['reservationStays'][0]['ReservationStayID'],
                    "arrivalDate": check_in_date.strftime("%Y-%m-%d"),
                    "departureDate": check_out_date.strftime("%Y-%m-%d"),
                    "adultCount": number_of_adults,
                    "childCount": number_of_children,
                    "roomTypeId": 2,
                    "rateAmount": rate_amount
                }
            ],
            "notes": notes
        }
        response = update_reservation(reservation_id, update_data)
        if "error" in response:
            st.error(f"Failed to update reservation: {response['error']}")
        else:
            st.success("Reservation updated successfully!")
            st.session_state.page = "update_reservation"
            st.rerun()  # Redirect to reservation list page

if __name__ == "__main__":
    main()
