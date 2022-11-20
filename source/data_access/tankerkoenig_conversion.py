import pandas as pd
from source.download_files.downloader import download_stations
from source.datetime_conversion.functions import convert_df_to_epoch_seconds_utc

PRICES_COLUMNS = ['timestamp', 'station_uuid', 'price_diesel', 'price_e5', 'price_e10']
PRICES_TANKERK_COLUMNS = ['date', 'station_uuid', 'diesel', 'e5', 'e10', 'dieselchange', 'e5change', 'e10change']
STATIONS_COLUMNS = ['uuid', 'name', 'brand', 'street', 'place', 'lat', 'lon']
STATIONS_TANKERK_COLUMNS = ['uuid', 'name', 'brand', 'street', 'house_number',
                            'post_code', 'city', 'latitude', 'longitude']

def load_prices_from_file(filepath: str):
    df_tk = pd.read_csv(filepath, sep=',', names=PRICES_TANKERK_COLUMNS, header=1)
    df = pd.DataFrame(columns=PRICES_COLUMNS)
    df['timestamp'] = convert_df_to_epoch_seconds_utc(df=df_tk, column='date')
    df['station_uuid'] = df_tk['station_uuid']
    df['price_diesel'] = df_tk['diesel']
    df['price_e5'] = df_tk['e5']
    df['price_e10'] = df_tk['e10']
    return df

def load_stations_from_file(filepath: str):
    df_tk = pd.read_csv(filepath, sep=',', names=STATIONS_TANKERK_COLUMNS, header=1)
    # convert from df_tk with STATIONS_TANKERK_COLUMNS to df with STATIONS_COLUMNS
    df = pd.DataFrame(columns=STATIONS_COLUMNS)
    print(df.shape, df_tk.shape, df_tk.dtypes)
    df['uuid'] = df_tk['uuid']
    df['name'] = df_tk['name']
    df['brand'] = df_tk['brand'].str.lower()
    df['street'] = df_tk['street'] + ' ' + df_tk['house_number']
    df['place'] = df_tk['post_code'] + ' ' + df_tk['city']
    df['lat'] = df_tk['latitude']
    df['lon'] = df_tk['longitude']
    return df




