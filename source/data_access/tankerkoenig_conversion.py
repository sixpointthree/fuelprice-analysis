import pandas as pd
from source.download_files.downloader import download_stations

PRICES_COLUMNS = ['id', 'timestamp', 'station_id', 'price_diesel', 'price_e5', 'price_e10']
PRICES_TANKERK_COLUMNS = ['date', 'station_uuid', 'diesel', 'e5', 'e10', 'dieselchange', 'e5change', 'e10change']
STATIONS_COLUMNS = ['id', 'uuid', 'name', 'brand', 'street', 'place', 'lat', 'lng']
STATIONS_TANKERK_COLUMNS = ['uuid', 'name', 'brand', 'street', 'house_number',
                            'post_code', 'city', 'latitude', 'longitude']

def load_prices_from_file(filepath: str):
    df = pd.read_csv(filepath, sep=',', names=PRICES_TANKERK_COLUMNS)
    df = df.drop(columns=['dieselchange', 'e5change', 'e10change'])
    # to-do
    # first we need to check if station_uuids are all available in stations table

    # if not, we need to download the stations file and add the missing stations to the stations table

def load_stations_from_file(filepath: str):
    df_tk = pd.read_csv(filepath, sep=',', names=STATIONS_TANKERK_COLUMNS, header=1)
    # convert from df_tk with STATIONS_TANKERK_COLUMNS to df with STATIONS_COLUMNS
    df = pd.DataFrame(columns=STATIONS_COLUMNS)
    print(df.shape, df_tk.shape, df_tk.dtypes)
    df['id'] = -1
    df['uuid'] = df_tk['uuid']
    df['name'] = df_tk['name']
    df['brand'] = df_tk['brand']
    df['street'] = df_tk['street'] + ' ' + df_tk['house_number']
    df['place'] = df_tk['post_code'] + ' ' + df_tk['city']
    df['lat'] = df_tk['latitude']
    df['lng'] = df_tk['longitude']
    return df




