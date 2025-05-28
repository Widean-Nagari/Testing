import streamlit as st
import streamlit.components.v1 as components
import datetime
import base64
import components.show_room_list as show_room_list
import components.show_guest_list as show_guest_list
import components.show_legend as show_legend
from api.reservation import get_reservations

# Streamlit app
def main():
    st.set_page_config(layout="wide")
    st.title("Room Plans")

    if "modal_open" not in st.session_state:
        st.session_state.modal_open = False

    # Date Picker
    start_date = st.date_input("Select a starting date", value=datetime.date.today())

    # Accordion Sections
    with st.expander("Room List", expanded=True):
        st.subheader("Room List")
        show_room_list.show(start_date)

    with st.expander("Unassigned Guest List", expanded=False):
        st.subheader("Unassigned Guest List")
        show_guest_list.show(start_date)

    with st.expander("Legend", expanded=False):
        st.subheader("Legend")
        show_legend.show()

if __name__ == "__main__":
    main()
