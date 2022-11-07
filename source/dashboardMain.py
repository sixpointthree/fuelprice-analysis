import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
from dateutil import tz

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

df_orig = pd.read_csv('data/mvp_station_prices_2019-10_omv_donzdorf.csv', sep=',')
df = df_orig

# filter petrol grade
list_petrolgrade = ['diesel', 'e5', 'e10']
st.sidebar.header("Filter here:")
selected_petrolgrade = st.sidebar.multiselect(
    "Select petrol grade:",
    options=list_petrolgrade,
    default=list_petrolgrade
)

# filter date range
date_range = st.sidebar.date_input("date range without default", [datetime.date(2019, 10, 1), datetime.date(2019, 10, 31)])
if len(date_range) != 2:
    st.write("Select date range")
else:
    EUR = tz.gettz('Europe / Berlin')
    from_datetime = datetime.datetime(date_range[0].year, date_range[0].month, date_range[0].day, 0, 0, 0, tzinfo=EUR).isoformat(sep=" ", timespec="seconds")
    to_datetime = datetime.datetime(date_range[1].year, date_range[1].month, date_range[1].day, 23, 59, 59, tzinfo=EUR).isoformat(sep=" ", timespec="seconds")
    df = df.query(
        "date >= @from_datetime and date <= @to_datetime"
    )


# show table
st.dataframe(df)

# -----Mainpage------
st.title("Fuelprice Dashboard")
st.markdown("##")

if selected_petrolgrade:
    left_col, right_col = st.columns([1, 2])
    with left_col:
        st.subheader("Barchart fuel price")
        fig_mean = px.bar(
            x=selected_petrolgrade,
            y=df.loc[1:, selected_petrolgrade].mean(axis=0),
            orientation="v",
            title="<b>Mean price per petrol grade </b>",
            color_discrete_sequence=["#0013B8"],
            template="plotly_white",
            )
        fig_mean.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )
        st.plotly_chart(fig_mean, use_container_width=True)

    with right_col:
        st.subheader("Lineplot fuel price")
        fig_fuelprice = px.line(
            df,
            x="date",
            y=selected_petrolgrade,
            title="<b> Price per petrol gate over time </b>",
            template="plotly_dark",
        )
        fig_fuelprice.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )
        st.plotly_chart(fig_fuelprice, use_container_width=True)
else:
    st.write("Select a petrol grade")

st.markdown("----")


hide_style = """
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html=True)
