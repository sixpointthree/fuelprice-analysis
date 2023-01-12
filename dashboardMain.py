import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
from dateutil import tz
from source.data_access.functions import get_prices_by_date_tz, check_stations_csv

UUID_OMV_DONZDORF = "16f07bfd-0bde-4126-a393-ea8a7d053283"
UUID_ARAL_GOEPPINGEN = "77c4cc3c-ae11-43c4-85cc-5c147409b46f"
UUID_SHELL_GOEPPINGEN = "c13f60cb-7e1c-40a8-b05a-157fd571b3fa"

MVP_UUIDS = [UUID_OMV_DONZDORF, UUID_ARAL_GOEPPINGEN, UUID_SHELL_GOEPPINGEN]

check_stations_csv()

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

# filter petrol grade
list_petrolgrade = ['diesel', 'e5', 'e10']
st.sidebar.header("Filter here:")
selected_petrolgrade_txt = st.sidebar.multiselect(
    "Select petrol grade:",
    options=list_petrolgrade,
    default=list_petrolgrade
)
selected_petrolgrade = []
for grade in selected_petrolgrade_txt:
    if grade == 'diesel':
        selected_petrolgrade.append('price_diesel')
    if grade == 'e5':
        selected_petrolgrade.append('price_e5')
    if grade == 'e10':
        selected_petrolgrade.append('price_e10')

# filter date range
date_range = st.sidebar.date_input(label="Select a date:",
                                   min_value=datetime.date(2014, 6, 8),
                                   max_value=datetime.date.today() - datetime.timedelta(days=1),
                                   value=(datetime.date.today() - datetime.timedelta(days=8), datetime.date.today() - datetime.timedelta(days=1)))
if len(date_range) != 2:
    st.write("Select date range")
    st.stop()
else:
    from_datetime = datetime.date(date_range[0].year, date_range[0].month, date_range[0].day)
    to_datetime = datetime.datetime(date_range[1].year, date_range[1].month, date_range[1].day)
    df = get_prices_by_date_tz(from_datetime, to_datetime, station_uuids=MVP_UUIDS, tz=tz.gettz('Europe/Berlin'))

# -----Mainpage------
st.title("Fuelprice Dashboard")
st.markdown("##")

if selected_petrolgrade:
    tab_hist_data, tab_prediction, tab_recommend = st.tabs(['historic data', 'prediction', 'recommendationfor action'])

    with tab_hist_data:
        left_col, right_col = st.columns([3, 10])
        # darstellung Durchschnitt, min, max der gewählten Spritsorten
        avg_price = df.loc[1:, selected_petrolgrade].mean(axis=0).round(decimals=2)
        min_price = df.loc[1:, selected_petrolgrade].min(axis=0).round(decimals=2)
        max_price = df.loc[1:, selected_petrolgrade].max(axis=0).round(decimals=2)

        with left_col:
            if len(selected_petrolgrade_txt) > 0:
                st.subheader(selected_petrolgrade_txt[0])
                st.write(f'Ø {avg_price[0]}€')
                st.caption(f'min: {min_price[0]}€')
                st.caption(f'max: {max_price[0]}€')

            if len(selected_petrolgrade_txt) > 1:
                st.markdown("----")
                st.subheader(selected_petrolgrade_txt[1])
                st.write(f'Ø {avg_price[1]}€')
                st.caption(f'min: {min_price[1]}€')
                st.caption(f'max: {max_price[1]}€')

            if len(selected_petrolgrade_txt) > 2:
                st.markdown("----")
                st.subheader(selected_petrolgrade_txt[2])
                st.write(f'Ø {avg_price[2]}€')
                st.caption(f'min: {min_price[2]}€')
                st.caption(f'max: {max_price[2]}€')

        with right_col:
            # Darstellung Preisverlauf in Lineplot
            st.subheader("Time course of selected fuel prices")
            fig_fuelprice = px.line(
                df,
                x="timestamp",
                y=selected_petrolgrade,
                title="<b> Price per petrol grade</b>",
                template="plotly_dark",
            )
            fig_fuelprice.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )
            st.plotly_chart(fig_fuelprice, use_container_width=True)
    with tab_prediction:
        # hier die vorhersagen
        st.write('Inhalt folgt')
    with tab_recommend:
        # hier Handlungsempfehlungen
        st.subheader('Recommendation in action:')
        st.write('~ Example ~')
        st.subheader('Based on:')
        st.write('~ Example ~')
else:
    st.write("Select a petrol grade")

# show table
st.dataframe(df)

st.markdown("----")

hide_style = """
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html=True)
