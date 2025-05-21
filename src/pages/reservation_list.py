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
        status = st.selectbox("Status", ["All", "confirmed", "checked-in", "checked-out", "cancelled"])
        date_range = st.date_input("Date range", [])
        search = st.text_input("Search by guest name or reservation ID")

    # Fetch data
    reservations = get_reservations(status, date_range, search)
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
        .status-confirmed {
            background-color: #d6e4ff;
            color: #4a6edb;
        }
        .status-checked-out {
            background-color: #d1f4d5;
            color: #3a785f;
        }
        </style>
        """, unsafe_allow_html=True)

        for idx, row in df.iterrows():
            if idx % 3 == 0:
                col1, col2, col3 = st.columns(3)
            with [col1, col2, col3][idx % 3]:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">{row['ReservationID']}</div>
                    <div style="margin-bottom: 28px;">{row['GuestName']}</div>
                    <div class="card-details">
                        <span>Property:</span><span>{row['Property']}</span>
                    </div>
                    <div class="card-details">
                        <span>Channel:</span><span>{row['Channel']}</span>
                    </div>
                    <div class="card-details">
                        <span>Reservation Date:</span><span>{row['ReservationDate']}</span>
                    </div>
                    <div class="card-footer">ID: {row['ID']}</div>
                    <div class="status-badge status-{row['Status'].lower().replace(' ', '-')}">{row['Status']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No reservations found.")

main()