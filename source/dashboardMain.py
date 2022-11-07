import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
from dateutil import tz

# Anaconda prompt:
# streamlit run dashboardDemo.py
#..\venv\Scripts\streamlit.exe run dashboardMain.py


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

df = pd.read_csv('data/mvp_station_prices_2019-10_omv_donzdorf.csv', sep=',')

d5 = st.date_input("date range without default", [datetime.date(2019, 10, 1), datetime.date(2019, 10, 31)])
st.write(d5)

EUR = tz.gettz('Europe / Berlin')
from_datetime = datetime.datetime(d5[0].year, d5[0].month, d5[0].day, 0, 0, 0, tzinfo= EUR).isoformat(sep=" ",timespec= "seconds")
to_datetime = datetime.datetime(d5[1].year, d5[1].month, d5[1].day, 23, 59, 59, tzinfo= EUR).isoformat(sep= " ",timespec= "seconds")
print(from_datetime)

df_selection = df.query(
    "date >= @from_datetime and date <= @to_datetime"
)

st.dataframe(df_selection)

# -----Mainpage------
st.title(":line_chart: fuelprice Dashboard")
st.markdown("##")

fuel_price_e5 = float(df["e5"].count())

#left_col = st.columns(1)
#with left_col:
#    st.subheader("Fuel price")


st.markdown("----")
fig_fuelprice = px.line(
    df_selection,
    x="date",
    y="e5",
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
