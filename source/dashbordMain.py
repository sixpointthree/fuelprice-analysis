import pandas as pd
import plotly.express as px
import streamlit as st
import datetime

# Anaconda prompt:
# cd C:\Users\lcami\Desktop\Master\Semester 1\BI\Projekt
# streamlit run dashboardDemo.py

# abort: strg c

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

df = pd.read_csv('mvp_station_prices_2019-10_omv_donzdorf.csv', sep=';')

d5 = st.date_input("date range without default", [datetime.date(2019, 10, 1), datetime.date(2019, 10, 31)])
st.write(d5)

df_selection = df.query(
    "date between @d5[0] and @d5[1]"
)

st.dataframe(df_selection)

# -----Mainpage------
st.title(":bar_chart: fuelprice Dashboard")
st.markdown("##")

fuel_price_e5 = float(df["e5"].count())

left_col = st.columns(1)
with left_col:
    st.subheader("Fuel price")


st.markdown("----")
fig_fuelprice = px.line(
    df_selection,
    x="Tag",
    y="Preis",
    title="<b> Fuel Price </b>",
    template="plotly_dark",
)
fig_fuelprice.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_fuelprice)

hide_style = """
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html=True)
