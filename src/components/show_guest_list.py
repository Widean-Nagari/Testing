import streamlit as st
import streamlit.components.v1 as components
import components.show_room_list as show_room_list
import components.show_legend as show_legend
from api.reservation import get_reservations

def show(start_date):
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

            show_room_list.show(start_date, 200)
            show_legend.show()
            st.button("Cancel", on_click=close_modal)

def open_modal():
    st.session_state.modal_open = True

def close_modal():
    st.session_state.modal_open = False
