import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
from dateutil import tz
from source.data_access.functions import get_prices_by_date_tz, check_stations_csv
from source.location.find_stations import find_stations_from_db_by_location
import pmdarima as pm

UUID_OMV_DONZDORF = "16f07bfd-0bde-4126-a393-ea8a7d053283"

station_desc = "Anton Schmid GmbH 6 Co KG, Brand: None, Address: Mozartstraße 33, 73072 Donzdorf"
station_uuid = UUID_OMV_DONZDORF

check_stations_csv()

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

# filter petrol grade
list_petrolgrade = ['price_diesel', 'price_e5', 'price_e10']
st.sidebar.header("Filter here:")

# add text input with submit button
with st.form(key='location_form'):
    location_input = st.text_input("Enter location:", value="shell esslingen")
    submit_button = st.form_submit_button(label='Find')

if submit_button:
    selected_stations = find_stations_from_db_by_location(location_input, 1)
    if len(selected_stations) < 1:
        st.write(f"No stations found for query: {location_input}")
    else:
        station = selected_stations.iloc[0]
        station_desc = f"{station['name']}, Brand: {station['brand']}, Address: {station['street']}, {station['place']}"
        print(station_desc)
        station_uuid = station['uuid']

selected_petrolgrade = st.sidebar.multiselect(
    "Select petrol grade:",
    options=list_petrolgrade,
    default=list_petrolgrade
)


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
    df = get_prices_by_date_tz(from_datetime, to_datetime, station_uuids=[station_uuid], tz=tz.gettz('Europe/Berlin'))

# -----Mainpage------
st.title("Fuelprice Dashboard")
st.write(f"Station:    {station_desc}")
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
            x="timestamp",
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

# show table
st.dataframe(df)

# show prediction model
st.title("Prediction for E5 Petrol")
TRAIN_START_DATE, TRAIN_END_DATE = datetime.date(2023, 1, 4), datetime.date(2023, 1, 11)
PREDICT_DATE = TRAIN_END_DATE + datetime.timedelta(days=1)

df_train = get_prices_by_date_tz(datetime.date(2023, 1, 4), datetime.date(2023, 1, 11),
                                 station_uuids=[UUID_OMV_DONZDORF], tz=tz.gettz('Europe/Berlin'))
print(df_train.head())
prediction_algorithm = st.radio(
    "Select prediction algorithm",
    ("Naive", "Seasonal Naive", "ARIMA(2,1,2)(1,1,1)[24]")
)

left_col, right_col = st.columns([2, 1])
with left_col:
    fig_train = px.line(
        df_train,
        x="timestamp",
        y="price_e5",
        title="<b> Training data </b>",
        template="plotly_dark",
    )
    fig_train.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    st.plotly_chart(fig_train, use_container_width=True)

with right_col:
    pred_data = {'timestamp': [], 'price_e5': [] }
    for hour in range(24):
        pred_data['timestamp'].append(datetime.datetime(PREDICT_DATE.year, PREDICT_DATE.month, PREDICT_DATE.day,
                                                        hour, 0, 0))
        pred_data['price_e5'].append(0.0)
    df_predict = pd.DataFrame(index=range(0, 24), columns=['timestamp', 'price_e5'],
                              data=pred_data)
    count_last_day = len(df_train[df_train['timestamp'].dt.date == TRAIN_END_DATE])
    if prediction_algorithm == "Naive":
        df_predict['price_e5'] = df_train['price_e5'].iloc[-1]

    elif prediction_algorithm == "Seasonal Naive":
        for hour in range(24):
            filter_datetime = datetime.datetime(year=TRAIN_END_DATE.year, month=TRAIN_END_DATE.month, day=TRAIN_END_DATE.day) + datetime.timedelta(hours=hour)
            # convert filter_datetime to datetime64[ns, tzfile('Europe/Berlin')] with pandas.to_datetime
            filter_datetime = pd.to_datetime(filter_datetime, utc=True).tz_convert('Europe/Berlin')
            print(filter_datetime)
            df_predict['price_e5'].iloc[hour] = df_train[df_train['timestamp'] <= filter_datetime].iloc[-1]['price_e5']
    elif prediction_algorithm == "ARIMA(2,1,2)(1,1,1)[24]":
        # TODO not sure if everything correct here
        # calculate ARIMA model. Use pmdarima package
        # https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.auto_arima.html

        # fit model with seasonal arima(2,1,2)(1,1,1)[count_last_day] and df_train['price_e5'] as input
        # https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.ARIMA.html
        model = pm.ARIMA(order=(2, 1, 2), seasonal_order=(1, 1, 1, count_last_day))
        model.fit(df_train['price_e5'].values)
        print(model.summary())
        # predict
        print(model.predict(n_periods=24))
        df_predict['price_e5'] = model.predict(n_periods=24)

    print(df_predict)
    fig_pred = px.line(
        df_predict,
        x="timestamp",
        y="price_e5",
        title="<b> Prediction </b>",
        template="plotly_dark",
    )
    fig_pred.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    # change color of prediction to red
    fig_pred.update_traces(line_color="#FF0000")
    st.plotly_chart(fig_pred, use_container_width=True)


st.markdown("----")


hide_style = """
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html=True)
