import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
import random
import os
import base64
from api.reservation import get_reservations

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        base64_bytes = base64.b64encode(img_file.read()).decode("utf-8")
    return base64_bytes

def show_room_list(start_date, height=600):
    day_count = 7
    st.write(f"Room information and calendar for the next {day_count} days.")
    dates = [(start_date + datetime.timedelta(days=i)).strftime("%a %d") for i in range(day_count)]
    current_date = start_date.strftime("%b %Y")

    rooms = [
        ["101", "Single", "1st Floor", "Sea View", "Balcony, King Bed", "No", "Yes"],
        ["102", "Double", "2nd Floor", "Mountain View", "Twin Beds, Fireplace", "Yes", "No"],
        ["103", "Suite", "3rd Floor", "City View", "Jacuzzi, King Bed", "No", "Yes"],
        ["104", "Deluxe", "4th Floor", "Garden View", "Balcony, Queen Bed", "No", "Yes"],
        ["105", "Presidential", "5th Floor", "Ocean View", "Private Pool, King Bed", "No", "Yes"]
    ]

    reservations = [
        ["101", "2025-05-27", "2025-05-29", "John Doe"],
        ["104", "2025-05-28", "2025-05-30", "Jane Doe"],
    ]

    valid_reservations = []
    for r in reservations:
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = (start_date + datetime.timedelta(days=day_count - 1)).strftime("%Y-%m-%d")
        if start_date_str <= r[1] <= end_date_str and start_date_str <= r[2] <= end_date_str:
            valid_reservations.append(r)
        elif r[1] < start_date_str and r[2] > end_date_str:
            r[1] = start_date_str
            r[2] = end_date_str
            valid_reservations.append(r)
        elif r[1] < start_date_str and start_date_str <= r[2] <= end_date_str:
            r[1] = start_date_str
            valid_reservations.append(r)
        elif r[2] > end_date_str and start_date_str <= r[1] <= end_date_str:
            r[2] = end_date_str
            valid_reservations.append(r)

    for reservation in valid_reservations:
        reservation[1] = datetime.datetime.strptime(reservation[1], "%Y-%m-%d").strftime("%a %d")
        reservation[2] = datetime.datetime.strptime(reservation[2], "%Y-%m-%d").strftime("%a %d")

    rows = "".join([
        f"<tr>"
        f"<td onmouseenter=\"showModal('Room Number: {room[0]}<br>Room Type: {room[1]}<br>Floor: {room[2]}<br>Exposure: {room[3]}<br>Attributes: {room[4]}<br>Smoking: {room[5]}<br>Clean: {room[6]}')\" onmouseleave=\"closeModal()\">{room[0]}</td>"
        f"<td onmouseenter=\"showModal('Room Number: {room[0]}<br>Room Type: {room[1]}<br>Floor: {room[2]}<br>Exposure: {room[3]}<br>Attributes: {room[4]}<br>Smoking: {room[5]}<br>Clean: {room[6]}')\" onmouseleave=\"closeModal()\">{room[1]}</td>"
        + "".join([
            f"<td>"
            f"<div style=\"display: flex;\">"
            f"{''.join([f'<div class=\"reservation-card\">{reservation[3]}</div>' for reservation in valid_reservations if reservation[0] == room[0] and dates.index(reservation[1]) <= i <= dates.index(reservation[2])])}"
            f"</div>"
            f"</td>"
            for i in range(day_count)
        ]) +
        "</tr>"
        for room in rooms
    ])

    components.html(f"""
    <div id=\"room-details-modal\" style=\"
        display: none;
        position: fixed;
        top: 10%;
        left: 50%;
        transform: translate(-50%, -20%);
        background-color: white;
        border: 1px solid #ddd;
        padding: 0 20px;
        z-index: 1000;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        font-family: Arial, sans-serif;
        overflow: auto;
    ">
        <h3>Room Details</h3>
        <p id=\"room-details-content\"></p>
    </div>
    <table border=\"1\" style=\"width: 100%; font-family: Arial, sans-serif; color: white;\">
        <tr>
            <th rowspan=\"2\">Room</th>
            <th rowspan=\"2\">Room Type</th>
            <th colspan={day_count}>{current_date}</th>
        </tr>
        <tr>
            {''.join([f'<th>{date}</th>' for date in dates])}
        </tr>
        {rows}
    </table>

    <style>
        .reservation-card {{
            background-color: #4CAF50;
            color: white;
            text-align: center;
            padding: 5px;
            border-radius: 5px;
            margin: 2px;
            font-size: 12px;
        }}
    </style>
    <script>
        function showModal(details) {{
            const modal = document.getElementById('room-details-modal');
            const content = document.getElementById('room-details-content');
            content.innerHTML = details;
            modal.style.display = 'block';
        }}

        function closeModal() {{
            const modal = document.getElementById('room-details-modal');
            modal.style.display = 'none';
        }}
    </script>
    """, height=height, scrolling=True)

def show_guest_list(start_date):
    # Fetch reservations from the API
    reservations = get_reservations(status=None, date_range=None, search=None)

    # Process the reservations data
    processed_reservations = []
    for reservation in reservations:
        profile = reservation.get("profile", {}).get("nameInfo", {})
        processed_reservations.append({
            "Last Name": profile.get("LastName", ""),
            "First Name": profile.get("FirstName", ""),
            "Confirmation Number": reservation.get("ConfirmationNumber", ""),
            "Room Type": "",  # Placeholder as Room Type is not in the example data
            "Rate Plan": "",  # Placeholder as Rate Plan is not in the example data
            "Average Nightly": "",  # Placeholder as Average Nightly is not in the example data
            "Departure Date": "",  # Placeholder as Departure Date is not in the example data
            "VIP Level": reservation.get("profile", {}).get("VIPStatusCode", ""),
        })

    if processed_reservations:
        # Create a DataFrame for better display
        rows = "".join([
            f"<tr>"
            f"<td>{reservation['Last Name']}</td>"
            f"<td>{reservation['First Name']}</td>"
            f"<td>{reservation['Confirmation Number']}</td>"
            f"<td>{reservation['Room Type']}</td>"
            f"<td>{reservation['Rate Plan']}</td>"
            f"<td>{reservation['Average Nightly']}</td>"
            f"<td>{reservation['Departure Date']}</td>"
            f"<td>{reservation['VIP Level']}</td>"
            "</tr>"
            for reservation in processed_reservations
        ])

        components.html(f"""
            <table border=\"1\" style=\"width: 100%; font-family: Arial, sans-serif; color: white; text-align: center;\">
                <tr>
                    <th>Last Name</th>
                    <th>First Name</th>
                    <th>Confirmation Number</th>
                    <th>Room Type</th>
                    <th>Rate Plan</th>
                    <th>Average Nightly</th>
                    <th>Departure Date</th>
                    <th>VIP Level</th>
                </tr>
                {rows}
            </table>

            <script>
                function openModal(lastName, firstName, confirmationNumber) {{
                    const modal = document.getElementById('fullscreen-modal');
                    modal.style.display = 'block';
                    document.getElementById('modal-title').innerText = `${{firstName}} ${{lastName}}`;
                    document.getElementById('modal-subtitle').innerText = `Confirmation Number: ${{confirmationNumber}}`;
                }}

                function closeModal() {{
                    const modal = document.getElementById('fullscreen-modal');
                    modal.style.display = 'none';
                }}
            </script>
        """, height=600, scrolling=True)
    else:
        st.write("No unassigned guests found.")

    st.button("Open Modal", on_click=open_modal)

    if st.session_state.modal_open:
        with st.container():
            # Title and subtitle
            st.title("Room")
            st.subheader("Dequarta Splinaria Umar, dr")

            # Search Criteria
            st.write("**Search Criteria**")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.text_input("Room Type:", "DLXK")
                st.checkbox("Retain Current Rate")
                st.text_input("Rate Reason:")
                st.checkbox("Show Assigned Rooms")
                st.checkbox("Show Unavailable Types")

            with col2:
                st.checkbox("Show Dirty", value=True)
                st.checkbox("Show Due Outs", value=True)
                st.text_input("Room Attributes")
                st.checkbox("Non-Smoking")
                st.checkbox("Accessible")
                st.checkbox("No Connecting Room")

            with col3:
                st.text_input("Connecting Room")
                st.selectbox("Building", ["Building 1", "Building 2"])
                st.selectbox("Wing", ["Wing A", "Wing B"])
                st.selectbox("Floor", ["1", "2", "3"])
                st.selectbox("Exposure", ["North", "South", "East", "West"])
                st.checkbox("Do not sort by Room Type")

            # Search Button
            st.button("Search")

            show_room_list(start_date, 200)
            show_legend()
            st.button("Cancel", on_click=close_modal)

def show_legend():
    attendant = get_base64_image("src/public/attendant.png")
    male = get_base64_image("src/public/male.png")
    female = get_base64_image("src/public/female.png")
    donotmove = get_base64_image("src/public/donotmove.png")
    vip = get_base64_image("src/public/vip.png")
    loyalty = get_base64_image("src/public/loyalty.png")
    share = get_base64_image("src/public/share.png")
    indirect = get_base64_image("src/public/indirect.png")
    clean = get_base64_image("src/public/clean.png")
    dirty = get_base64_image("src/public/dirty.png")
    inspect = get_base64_image("src/public/inspect.png")
    pickup = get_base64_image("src/public/pickup.png")
    turndown = get_base64_image("src/public/turndown.png")
    components.html(f"""
    <style>
        .legend {{
            color: white;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 5px 10px;
        }}

        .color-box {{
            width: 32px;
            height: 32px;
            display: inline-block;
            margin-right: 5px;
        }}

        .icon-placeholder {{
            width: 32px;
            height: 32px;
            display: inline-block;
            margin-right: 5px;
            background-size: contain;
            background-repeat: no-repeat;
        }}

        /* Define colors (same as image) */
        .in-house {{ background-color: #77c043; }}
        .reserved {{ background-color: #f8a44c; }}
        .pre-registered {{ background-color: #e74857; }}
        .out-of-order {{ background-color: #ccc; }}
        .room-hold {{ background-color: #30bfbf; }}
        .lease {{ background-color: #d692e0; }}
        .not-in-inventory {{ background-color: #111; }}
        .occupied {{ background-color: #c1dc42; }}

        /* Placeholder URLs for icons */
        .attendant-icon {{ background-image: url('data:image/png;base64,{attendant}'); }}
        .male-icon {{ background-image: url('data:image/png;base64,{male}'); }}
        .female-icon {{ background-image: url('data:image/png;base64,{female}'); }}
        .do-not-move-icon {{ background-image: url('data:image/png;base64,{donotmove}'); }}
        .vip-icon {{ background-image: url('data:image/png;base64,{vip}'); }}
        .loyalty-icon {{ background-image: url('data:image/png;base64,{loyalty}'); }}
        .share-icon {{ background-image: url('data:image/png;base64,{share}'); }}
        .indirect-icon {{ background-image: url('data:image/png;base64,{indirect}'); }}
        .clean-icon {{ background-image: url('data:image/png;base64,{clean}'); }}
        .dirty-icon {{ background-image: url('data:image/png;base64,{dirty}'); }}
        .inspect-icon {{ background-image: url('data:image/png;base64,{inspect}'); }}
        .pickup-icon {{ background-image: url('data:image/png;base64,{pickup}'); }}
        .turn-down-icon {{ background-image: url('data:image/png;base64,{turndown}'); }}
    </style>
    <div class="legend">
        <div class="legend-item">
            <span class="color-box in-house"></span> In House
        </div>
        <div class="legend-item">
            <span class="color-box reserved"></span> Reserved
        </div>
        <div class="legend-item">
            <span class="color-box pre-registered"></span> Pre-registered
        </div>
        <div class="legend-item">
            <span class="color-box out-of-order"></span> Out Of Order
        </div>
        <div class="legend-item">
            <span class="color-box room-hold"></span> Room Hold
        </div>
        <div class="legend-item">
            <span class="color-box lease"></span> Lease
        </div>
        <div class="legend-item">
            <span class="color-box not-in-inventory"></span> Not in Inventory
        </div>
        <div class="legend-item">
            <span class="icon-placeholder attendant-icon"></span> Attendant in Room
        </div>
        <div class="legend-item">
            <span class="icon-placeholder male-icon"></span> Male
        </div>
        <div class="legend-item">
            <span class="icon-placeholder female-icon"></span> Female
        </div>
        <div class="legend-item">
            <span class="icon-placeholder do-not-move-icon"></span> Do Not Move
        </div>
        <div class="legend-item">
            <span class="icon-placeholder vip-icon"></span> VIP
        </div>
        <div class="legend-item">
            <span class="icon-placeholder loyalty-icon"></span> Loyalty Member
        </div>
        <div class="legend-item">
            <span class="icon-placeholder share-icon"></span> Share
        </div>
        <div class="legend-item">
            <span class="icon-placeholder indirect-icon"></span> Indirect
        </div>
        <div class="legend-item">
            <span class="icon-placeholder clean-icon"></span> Clean
        </div>
        <div class="legend-item">
            <span class="icon-placeholder dirty-icon"></span> Dirty
        </div>
        <div class="legend-item">
            <span class="icon-placeholder inspect-icon"></span> Inspect
        </div>
        <div class="legend-item">
            <span class="icon-placeholder pickup-icon"></span> Pickup
        </div>
        <div class="legend-item">
            <span class="icon-placeholder turn-down-icon"></span> Turn Down
        </div>
    </div>
    """, height=100)

def open_modal():
    st.session_state.modal_open = True

def close_modal():
    st.session_state.modal_open = False

# Streamlit app
def main():
    st.set_page_config(layout="wide")
    st.title("Room Plans")

    if "modal_open" not in st.session_state:
        st.session_state.modal_open = False

    # Date Picker
    start_date = st.date_input("Select a starting date", value=datetime.date.today())

    # Accordion Sections
    with st.expander("Room List", expanded=False):
        st.subheader("Room List")
        show_room_list(start_date)

    with st.expander("Unassigned Guest List", expanded=True):
        st.subheader("Unassigned Guest List")
        show_guest_list(start_date)

    with st.expander("Legend", expanded=False):
        st.subheader("Legend")
        show_legend()

if __name__ == "__main__":
    main()