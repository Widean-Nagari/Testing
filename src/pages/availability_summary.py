import streamlit as st
import pandas as pd
import datetime
import random
import numpy as np

# Streamlit app
def main():
    st.set_page_config(layout="wide")

    st.title("Hotel Booking Availability Summary")

    # Date Picker
    start_date = st.date_input("Select a starting date", value=datetime.date.today())
    dates = pd.date_range(start_date, periods=7)

    # Sample data generation (imitating the screenshot)
    room_types = [
        "DBPK - Deluxe Balcony Pool View King",
        "DBPT - Deluxe Balcony Pool View Twin",
        "DLBT - Deluxe Balcony Twin",
        "DLXK - Deluxe King",
        "FRSK - Family Room Suite King",
        "GLSK - Gallery Suite King",
        "HILK - Hillside Studio King",
        "PRBK - Premier Balcony King",
        "PRBT - Premier Balcony Twin",
        "PRRK - Premier King",
        "PRSK - Premier Suite King",
        "PRRT - Premier Twin"
    ]

    # Inventory Summary
    st.subheader("Summary")
    st.markdown("""<div style='display: flex; gap: 20px;'>
        <div><strong style='color: white;'>123</strong> Count</div>
        <div><strong style='color: purple;'>123</strong> Percentage of Total</div>
        <div><strong style='color: green;'>123</strong> Available</div>
    </div>""", unsafe_allow_html=True)
    sum_data = {
        "Date": dates.strftime("%b %d, %Y"),
        "Inventory": [120, 122, 122, 122, 122, 122, 122],
        "Sold": [45, 54, 42, 27, 27, 46, 45],
    }
    sum_data["Available"] = [inv - sold for inv, sold in zip(sum_data["Inventory"], sum_data["Sold"])]
    sum_data["Opportunity"] = [0] * 7
    sum_data["Minimum Sellable"] = sum_data["Available"]

    # Create transposed summary display with values and percentage in split cells
    summary_html = """
    <table border="1" style="border-collapse: collapse; text-align: center; width: 100%;">
        <tr><th></th>{}</tr>
        <tr><th></th>{}</tr>
    """.format(
        "".join(f"<th colspan='2'>{date}</th>" for date in sum_data["Date"]),
        "".join(f"<th colspan='2'>{date.strftime('%A').upper()}</th>" for date in dates)
    )

    for category in ["Inventory", "Sold", "Available", "Opportunity", "Minimum Sellable"]:
        summary_html += f"<tr><td><b>{category}</b></td>"
        for i in range(7):
            val = sum_data[category][i]
            total = sum_data["Inventory"][i]
            pct = f"{(val / total * 100):.0f}" if total else "0"
            color = "white" if category != "Available" else "green"
            percent_color = "purple" if category != "Available" else "green"
            summary_html += f"<td style='color: {color};'>{val}</td><td style='color: {percent_color};'>{pct}%</td>"
        summary_html += "</tr>"

    summary_html += "</table>"
    st.markdown(summary_html, unsafe_allow_html=True)

    # Room Type Details with HTML table for percentage per cell
    detail_table = """
    <table border="1" style="border-collapse: collapse; text-align: center; font-size: 14px; width: 100%;">
        <thead>
            <tr><th></th>{}</tr>
            <tr><th>Room Types</th>{}</tr>
        </thead>
        <tbody>
    """.format(
        "".join(f"<th colspan='2'>{date.strftime('%b %d, %Y')}</th>" for date in dates),
        "".join(f"<th colspan='2'>{date.strftime('%A').upper()}</th>" for date in dates)
    )

    details_data = {
        "DBPK - Deluxe Balcony Pool View King": {
            'max': 8,
            'data': [5, 5, 3, 5, 6, 4, 4]
        },
        "DBPT - Deluxe Balcony Pool View Twin": {
            'max': 2,
            'data': [1, 1, 1, 1, 1, 1, 2]
        },
        "DLBT - Deluxe Balcony Twin": {
            'max': 12,
            'data': [0, 2, 5, 7, 9, 4, 0]
        },
        "DLXK - Deluxe King": {
            'max': 28,
            'data': [14, 12, 3, 12, 10, 5, 9]
        },
        "FRSK - Family Room Suite King": {
            'max': 8,
            'data': [6, 3, 8, 8, 8, 3, 7]
        },
        "GLSK - Gallery Suite King": {
            'max': 4,
            'data': [2, 1, 3, 3, 3, 3, 3]
        },
        "HILK - Hillside Studio King": {
            'max': 16,
            'data': [13, 13, 3, 14, 10, 9, 14]
        },
        "PRBK - Premier Balcony King": {
            'max': 12,
            'data': [10, 11, 12, 12, 12, 9, 12]
        },
        "PRBT - Premier Balcony Twin": {
            'max': 9,
            'data': [7, 8, 9, 9, 9, 6, 8]
        },
        "PRRK - Premier King": {
            'max': 12,
            'data': [10, 7, 11, 12, 12, 6, 6]
        },
        "PRSK - Premier Suite King": {
            'max': 4,
            'data': [0, 0, 0, 4, 3, 3, 3]
        },
        "PRRT - Premier Twin": {
            'max': 9,
            'data': [7, 5, 9, 8, 8, 7, 9]
        }
    }
    for room_type in room_types:
        inventory_per_day = details_data[room_type]['max']
        detail_table += "<tr><td style='text-align: left; display: flex; justify-content: space-between;'>"
        detail_table += f"<span>{room_type}</span>"
        detail_table += f"<span style='color: purple; background-color: #ffffcc; width: 24px; font-weight: bold; text-align: center;'>{inventory_per_day}</span>"
        detail_table += "</td>"
        counts = details_data[room_type]['data']
        for i, count in enumerate(counts):
            pct = f"{(count / inventory_per_day) * 100:.0f}" if inventory_per_day else "0"
            detail_table += f"<td>{count}</td><td style='color: purple;'>{pct}%</td>"
        detail_table += "</tr>"

    detail_table += "</tbody></table>"

    # Expandable details section

    st.subheader("Details")
    st.markdown("""<div style='display: flex; gap: 20px;'>
        <div><strong style='color: white;'>123</strong> Count</div>
        <div><strong style='color: red;'>*</strong> Overbooking Limit</div>
        <div><strong style='color: purple;'>123</strong> Percentage of Total</div>
        <div><strong style='color: green;'>123</strong> Available</div>
        <div><input type='checkbox' disabled> Suite Component</div>
        <div><strong style='color: purple; background-color: #ffffcc; padding: 0 4px'>123</strong> Physical Inventory</div>
    </div>""", unsafe_allow_html=True)
    st.markdown(detail_table, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
