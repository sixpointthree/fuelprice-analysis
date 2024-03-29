import dateutil.tz

from .db_model import Prices, Stations, Session, PRICES_TABLE_NAME, STATIONS_TABLE_NAME
import pandas as pd
from source.download_files.downloader import download_prices, download_station
from source.data_access.tankerkoenig_conversion import load_prices_from_file, load_stations_from_file
import datetime
import os
from sqlalchemy import types
from geographiclib.geodesic import Geodesic


# trigger download of requested date
# change format from tankerkoenig to db format

# get station info for a given station uuid
def get_station_info_uuid(station_uuid: str):
    with Session() as session:
        data = session.query(Stations).filter(
            Stations.uuid == station_uuid
        ).all()
        if len(data) < 0:
            raise ValueError(f'No station with uuid {station_uuid} found')
        return data[0]


def get_all_stations():
    with Session() as session:
        data = session.query(Stations).all()
        return data

def get_stations_by_coords(lat: float, lon: float, radius_km: float) -> pd.DataFrame:
    geod = Geodesic.WGS84

    theta = 0  # direction from North, clockwise
    azi1 = theta - 90  # (90 degrees to the left)
    shift = radius_km * 1000  # meters

    g_west = geod.Direct(lat, lon, azi1, shift)
    lon_west = g_west['lon2']

    g_east = geod.Direct(lat, lon, -azi1, shift)
    lon_east = g_east['lon2']

    lat_north = lat + radius_km / 111.3
    lat_south = lat - radius_km / 111.3

    with Session() as session:
        df = pd.read_sql(session.query(Stations).filter(
            Stations.lat >= lat_south,
            Stations.lat <= lat_north,
            Stations.lon >= lon_west,
            Stations.lon <= lon_east
        ).statement, session.bind)
        if len(df) == 0:
            raise ValueError(f'No stations found in radius {radius_km}km around {lat}, {lon}')
        return df


def add_station(station_uuid: str, name: str, brand: str, street: str, place: str, lat: float, lng: float):
    # check max id of station_id
    with Session() as session:
        max_id = session.query(Stations.id).order_by(Stations.id.desc()).first()
        if max_id is None:
            max_id = 0
        else:
            max_id = max_id['id']
        station = Stations(id=max_id + 1, uuid=station_uuid, name=name, brand=brand,
                           street=street, place=place, lat=lat, lng=lng)
        session.add(station)
        session.commit()


def add_stations(df: pd.DataFrame):
    with Session() as session:
        df.to_sql(name=STATIONS_TABLE_NAME, con=session.bind, if_exists='append', index=False, dtype={
            'uuid': types.String,
            'name': types.String,
            'brand': types.String,
            'street': types.String,
            'place': types.String,
            'lat': types.Float(precision=5),
            'lng': types.Float(precision=5)
        })


def add_prices(df: pd.DataFrame):
    with Session() as session:
        df.to_sql(name=PRICES_TABLE_NAME, con=session.bind, if_exists='append', index=False, dtype={
            'timestamp': types.Integer,
            'station_uuid': types.VARCHAR(length=36),
            'price_diesel': types.Float(precision=3),
            'price_e5': types.Float(precision=3),
            'price_e10': types.Float(precision=3)
        })
        session.commit()


def __read_df_from_db(from_datetime: int, to_datetime: int):
    with Session() as session:
        return pd.read_sql(session.query(Prices).filter(
            Prices.timestamp >= from_datetime,
            Prices.timestamp <= to_datetime
        ).statement, session.bind)

def __read_df_from_db_stations(from_datetime: int, to_datetime: int, station_uuids: list = None):
    with Session() as session:
        return pd.read_sql(session.query(Prices).filter(
            Prices.timestamp >= from_datetime,
            Prices.timestamp <= to_datetime,
            Prices.station_uuid.in_(station_uuids)
        ).statement, session.bind)


def get_prices_by_date_tz(from_date: datetime.date, to_date: datetime.date, station_uuids: list = None,
                          tz: dateutil.tz.tzfile = dateutil.tz.gettz('UTC')):
    from_datetime = int(datetime.datetime.combine(from_date, datetime.time.min).replace(tzinfo=tz).timestamp())
    to_datetime = int(datetime.datetime.combine(to_date, datetime.time.max).replace(tzinfo=tz).timestamp())
    df = get_prices(from_datetime, to_datetime, station_uuids)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert(tz)
    return df
def get_prices(from_datetime: int, to_datetime: int, station_uuids: list = None):
    # get data from database
    if station_uuids is None:
        df = __read_df_from_db(from_datetime=from_datetime, to_datetime=to_datetime)
    else:
        df = __read_df_from_db_stations(from_datetime=from_datetime, to_datetime=to_datetime, station_uuids=station_uuids)
    if len(df) > 0:
        print(df.columns)
        df_existing_dates = pd.to_datetime(df['timestamp'], unit='s').dt.date
    else:
        print(f'Did not find any records in database for {from_datetime} to {to_datetime}')
        df_existing_dates = None
    from_datetime_dt = datetime.datetime.fromtimestamp(from_datetime).date()
    to_datetime_dt = datetime.datetime.fromtimestamp(to_datetime).date()
    diff = to_datetime_dt - from_datetime_dt
    missing_list_dates = []
    for i in range(diff.days + 1):
        date = from_datetime_dt + datetime.timedelta(days=i)
        if df_existing_dates is None or date not in df_existing_dates.values:
            missing_list_dates.append(date)

    # check if data is empty
    if len(missing_list_dates) > 0:
        # to-do check if data is available at all
        # try to download the data
        print(f'Downloading {len(missing_list_dates)} data sets for {missing_list_dates}')
        for date in missing_list_dates:
            download_path = f'prices_{date.year}-{date.month}-{date.day}.csv'
            download_prices(year=date.year, month=date.month, day=date.day, target_path=download_path)
            df_temp = load_prices_from_file(filepath=download_path)
            add_prices(df_temp)
            print(f'Added {len(df_temp)} records for {date}')
            # remove file
            os.remove(download_path)
        if station_uuids is None:
            df = __read_df_from_db(from_datetime=from_datetime, to_datetime=to_datetime)
        else:
            df = __read_df_from_db_stations(from_datetime=from_datetime, to_datetime=to_datetime,
                                            station_uuids=station_uuids)
        return df
    else:
        return df



# load a range of datetime values from the database with datetime format iso8601
# and return them as a pandas dataframe
def get_data_from_db_iso8601(from_datetime: str, to_datetime: str):
    # convert from_datetime to seconds since epoch and check conversion
    from_datetime_seconds = int(datetime.datetime.fromisoformat(from_datetime).timestamp())
    to_datetime_seconds = int(datetime.datetime.fromisoformat(to_datetime).timestamp())
    return get_prices(from_datetime=from_datetime_seconds, to_datetime=to_datetime_seconds)


def check_stations_csv():
    with Session() as session:
        len_stations_db = len(session.query(Stations).all())
        if len_stations_db > 0:
            print('Stations already in database')
            return
        filename = 'stations.csv'
        download_station(target_path=filename)
        df = load_stations_from_file(filepath=filename)
        os.remove(filename)
        add_stations(df)
