import pandas as pd
import plotly.express as px
import streamlit as st

# Anaconda prompt:
# cd C:\Users\lcami\Desktop\Master\Semester 1\BI\Projekt
# streamlit run dashboardDemo.py

#abort: strg c

#emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

df=pd.read_csv('Oilprice.csv', sep=';')


st.sidebar.header("Filter here:")
currency=st.sidebar.multiselect(
    "Select currency:",
    options=df["Währung"].unique(),
    default=df["Währung"].unique()
)

df_selection=df.query(
    "Währung == @currency"
)

st.dataframe(df_selection)

#-----Mainpage------
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

total_sales =int(df_selection["Datum"].count())
price = round(df_selection["Eröffnung"].mean())
left_col, right_col= st.columns(2)
with left_col:
    st.subheader("Total Sales")
    st.subheader(f"{total_sales:,}")
with right_col:
    st.subheader("Average price")
    st.subheader(f"{price}")    

st.markdown("----")
fig_currency=px.bar(
    df_selection,
    x="Eröffnung",
    y="Währung",
    orientation="h",    #horizontal barchart
    title="<b>Sales currency </b>",
    color_discrete_sequence=["#0083B8"]*total_sales,
    template="plotly_white",
    )
fig_currency.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


st.plotly_chart(fig_currency)

hide_style= """
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html=True)