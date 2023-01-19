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
list_petrolgrade = ['Diesel', 'E5', 'E10']
st.sidebar.header("Filter here:")
selected_petrolgrade_txt = st.sidebar.multiselect(
    "Select petrol grade:",
    options=list_petrolgrade,
    default=list_petrolgrade
)
selected_petrolgrade = []
for grade in selected_petrolgrade_txt:
    if grade == 'Diesel':
        selected_petrolgrade.append('price_diesel')
    if grade == 'E5':
        selected_petrolgrade.append('price_e5')
    if grade == 'E10':
        selected_petrolgrade.append('price_e10')

# filter date range
date_range = st.sidebar.date_input(label="Select a date:",
                                   min_value=datetime.date(2014, 6, 8),
                                   max_value=datetime.date.today() - datetime.timedelta(days=1),
                                   value=(datetime.date.today() - datetime.timedelta(days=8), datetime.date.today() - datetime.timedelta(days=1)))

# filter location:
# text input with submit button
with st.sidebar.form(key='location_form'):
    location_input = st.text_input("Enter location:", value="shell esslingen")
    submit_button = st.form_submit_button(label='Find')

if submit_button:
    selected_stations = find_stations_from_db_by_location(location_input, 1)
    if len(selected_stations) < 1:
        st.sidebar.write(f"No stations found for query: {location_input}")
    else:
        station = selected_stations.iloc[0]
        station_desc = (f"Station: {station['name']}, Brand: {station['brand']}, Address: {station['street']}, {station['place']}")
        print(station_desc)
        station_uuid = station['uuid']
st.sidebar.write(station_desc)

if len(date_range) != 2:
    st.write("Select date range")
    st.stop()
else:
    from_datetime = datetime.date(date_range[0].year, date_range[0].month, date_range[0].day)
    to_datetime = datetime.datetime(date_range[1].year, date_range[1].month, date_range[1].day)
    df = get_prices_by_date_tz(from_datetime, to_datetime, station_uuids=[station_uuid], tz=tz.gettz('Europe/Berlin'))

# -----Mainpage------
st.title("Fuelprice Dashboard")
st.markdown("##")

if selected_petrolgrade:
    tab_hist_data, tab_prediction, tab_recommend = st.tabs(['Historic data', 'Prediction', 'Recommendation for action'])

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
                # set title to Price per petrol grade, then write the station_desc in a new line
                title=f"Price per petrol grade<br><span style='font-size: 0.8em; color: gray'>{station_desc}</span>",
                template="plotly_dark",
            )
            fig_fuelprice.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )
            st.plotly_chart(fig_fuelprice, use_container_width=True)
    with tab_prediction:
        # show prediction model
        st.title("Prediction for E5 Petrol")
        TRAIN_START_DATE, TRAIN_END_DATE = datetime.date(2023, 1, 4), datetime.date(2023, 1, 11)
        PREDICT_DATE = TRAIN_END_DATE + datetime.timedelta(days=1)

        df_train = get_prices_by_date_tz(datetime.date(2023, 1, 4), datetime.date(2023, 1, 11),
                                         station_uuids=[UUID_OMV_DONZDORF], tz=tz.gettz('Europe/Berlin'))
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
            pred_data = {'timestamp': [], 'price_e5': []}
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
                    filter_datetime = datetime.datetime(year=TRAIN_END_DATE.year, month=TRAIN_END_DATE.month,
                                                        day=TRAIN_END_DATE.day) + datetime.timedelta(hours=hour)
                    # convert filter_datetime to datetime64[ns, tzfile('Europe/Berlin')] with pandas.to_datetime
                    filter_datetime = pd.to_datetime(filter_datetime, utc=True).tz_convert('Europe/Berlin')
                    df_predict['price_e5'].iloc[hour] = df_train[df_train['timestamp'] <= filter_datetime].iloc[-1][
                        'price_e5']
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
    with tab_recommend:
        # hier Handlungsempfehlungen
        st.subheader('Recommendation in action:')
        st.write('~ Example ~')
        st.subheader('Based on:')
        st.write('~ Example ~')
else:
    st.write("Select a petrol grade")

# show table
# st.dataframe(df)


st.markdown("----")

hide_style = """
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html=True)
