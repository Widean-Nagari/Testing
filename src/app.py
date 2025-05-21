# src/app.py
import streamlit as st
import numpy as np
import time

import pandas as pd
import altair as alt

@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")

    st.button("Rerun")

def area_chart():
    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.subheader("Gross agricultural production ($B)")
            st.dataframe(data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(f"This demo requires internet access. Connection error: {e.reason}")

def line_chart():
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text(f"{i}% complete")
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

def other_chart():
    df = pd.DataFrame(
        # np.abs(np.random.randn(10, 3)),
        np.round(np.random.uniform(low=1, high=10, size=(10, 3))),
        columns=["a", "b", "c"],
    )
    st.bar_chart(df)
    st.line_chart(df)
    st.area_chart(df)
    st.dataframe(df)
    # st.table(df)

def main():
    st.set_page_config(page_title="Hotel Reservation Admin Dashboard", layout="wide")
    st.title("Hotel Reservation")

    area_chart()
    line_chart()
    other_chart()

if __name__ == "__main__":
    main()
