# src/pages/reservation_list.py
import streamlit as st
import pandas as pd
from api.reservations import get_reservations
from components.reservation_table import reservation_table

def main():
    st.set_page_config(page_title="Hotel Reservation Admin Dashboard", layout="wide")
    st.title("Reservation List")
    st.markdown("Manage all hotel reservations below.")

    # Filters
    with st.expander("Filters", expanded=True):
        status = st.selectbox("Status", ["All", "reserved", "checked in", "checked out", "cancelled"])
        date_range = st.date_input("Date range", [])

        search = st.text_input("Search by guest name or reservation ID", key="search_query")

    # Fetch data
    all_reservations = get_reservations(None, None, None)  # Fetch all reservations initially

    # Filter data dynamically based on inputs
    filtered_reservations = [
        r for r in all_reservations
        if (status == "All" or r.get("StatusCode", "").lower() == status.lower())
        and (not date_range or (
            pd.to_datetime(r.get("reservationStay", {}).get("ArrivalDate", "")).tz_localize(None) >= pd.to_datetime(date_range[0])
            and pd.to_datetime(r.get("reservationStay", {}).get("DepartureDate", "")).tz_localize(None) <= pd.to_datetime(date_range[1]) if len(date_range) == 2 else True
        ))
        and (not search or search.lower() in r.get("profile", {}).get("nameInfo", {}).get("FirstName", "").lower()
             or search.lower() in r.get("profile", {}).get("nameInfo", {}).get("LastName", "").lower()
             or search.lower() in r.get("ConfirmationNumber", "").lower())
    ]

    reservations = filtered_reservations
    if not reservations:
        st.info("No reservations found.")
        return
    df = pd.DataFrame(reservations)

    # Responsive card grid layout for reservations
    if not df.empty:
        st.markdown("""
        <style>
        .card {
            border-radius: 8px;
            border: 1px solid #ffffff;
            padding: 16px;
            margin: 8px;
            position: relative;
            font-size: 20px;
        }
        .card-header {
            font-weight: bold;
            font-size: 24px;
            text-transform: uppercase;
            color: white;
        }
        .card-details {
            display: flex;
            justify-content: space-between;
            margin: 4px 0;
        }
        .card-footer {
            font-size: 16px;
            color: 	#c4c7cb;
            margin-top: 8px;
            text-align: right;
            border-top: 1px solid #ffffff;
            padding-top: 8px;
        }
        .status-badge {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 4px 12px;
            border-radius: 32px;
            font-size: 16px;
            color: white;
        }
        .status-reserved {
            background-color: #d6e4ff;
            color: #4a6edb;
        }
        .status-checked-out {
            background-color: #d1f4d5;
            color: #3a785f;
        }
        .update-button {
            position: relative;
            top: 4px;
            background-color: #d6e4ff;
            padding: 8px 16px;
            border-radius: 4px;
        }
        </style>
        """, unsafe_allow_html=True)

        for idx, row in df.iterrows():
            if idx % 3 == 0:
                col1, col2, col3 = st.columns(3)
            with [col1, col2, col3][idx % 3]:
                guestNameInfos = row.profile['nameInfo']
                guestName = guestNameInfos['NamePrefix'] + " " + guestNameInfos['FirstName'] + " " + guestNameInfos['MiddleName'] + " " + guestNameInfos['LastName'] + " " + guestNameInfos['NameSuffix']
                dt = pd.to_datetime(row.ReservationDate).tz_convert(None)  # Convert to naive datetime
                reservationDate = dt.strftime("%-m/%-d/%Y")
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">{row.ConfirmationNumber}</div>
                    <div style="margin-bottom: 28px;">{guestName}</div>
                    <div class="card-details">
                        <span>Property:</span><span>{row.property['PropertyName']}</span>
                    </div>
                    <div class="card-details">
                        <span>Channel:</span><span>{row.BookingChannelCode}</span>
                    </div>
                    <div class="card-details">
                        <span>Reservation Date:</span><span>{reservationDate}</span>
                    </div>
                    <div class="card-footer">
                        <a class="update-button" href="/update_reservation?id={row.ReservationID}" target="_self" style="margin-right: 10px; text-decoration: none;">Update</a>
                        ID: {row.ReservationID}
                    </div>
                    <div class="status-badge status-{row.StatusCode.lower().replace(' ','-')}">{row.StatusCode}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No reservations found.")

main()