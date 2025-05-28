# src/components/reservation_table.py
import streamlit as st

def reservation_table(df):
    a = 1
    # st.dataframe(df, use_container_width=True)
    # for idx, row in df.iterrows():
    #     cols = st.columns([1,1,1,1,1,1,1,2])
    #     cols[0].write(row["ReservationID"])
    #     cols[1].write(row["GuestName"])
    #     cols[2].write(row["RoomNumber"])
    #     cols[3].write(row["RoomType"])
    #     cols[4].write(row["CheckIn"])
    #     cols[5].write(row["CheckOut"])
    #     cols[6].write(row["Status"])
    #     with cols[7]:
    #         if st.button("View", key=f"view_{row['ReservationID']}"):
    #             st.experimental_set_query_params(page="detail", id=row["ReservationID"])
    #         if st.button("Edit", key=f"edit_{row['ReservationID']}"):
    #             # st.experimental_set_query_params(page="detail", id=row["ReservationID"])
    #             st.warning("Update not implemented in prototype.")
    #         if st.button("Delete", key=f"delete_{row['ReservationID']}"):
    #             st.warning("Delete not implemented in prototype.")
