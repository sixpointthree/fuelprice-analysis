from .db_model import Prices, Stations, Session
import pandas as pd
from source.download_files.downloader import download_prices, download_station
from source.data_access.tankerkoenig_conversion import load_prices_from_file, load_stations_from_file
import datetime


# trigger download of requested date
# change format from tankerkoenig to db format

# get station info for a given station id
def get_station_info(station_id: int):
    with Session() as session:
        data = session.query(Stations).filter(
            Stations.id == station_id
        ).all()
        return data

# get station info for a given station uuid
def get_station_info_uuid(station_uuid: str):
    with Session() as session:
        data = session.query(Stations).filter(
            Stations.uuid == station_uuid
        ).all()
        return data

def get_all_stations():
    with Session() as session:
        data = session.query(Stations).all()
        return data

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
        max_id = session.query(Stations.id).order_by(Stations.id.desc()).first()
        if max_id is None:
            max_id = 0
        else:
            max_id = max_id['id']
        list_stations = []
        for index, row in df.iterrows():
            station = Stations(id=max_id + 1, uuid=row['uuid'], name=row['name'], brand=row['brand'],
                               street=row['street'], place=row['place'], lat=row['lat'], lng=row['lng'])
            list_stations.append(station)
            max_id += 1
        session.bulk_save_objects(list_stations)
        session.commit()

# load a range of datetime values from the database
# and return them as a pandas dataframe
def get_data_from_db(from_datetime: int, to_datetime: int):
    with Session() as session:
        # get data from database
        data = session.query(Prices).filter(
            Prices.date >= from_datetime,
            Prices.date <= to_datetime
        ).all()
        # check if data is empty
        if len(data) == 0:
            # to-do check if data is available at all
            # try to download the data
            from_datetime_iso8601 = datetime.datetime.fromtimestamp(from_datetime)
            to_datetime_iso8601 = datetime.datetime.fromtimestamp(to_datetime)
            diff = datetime.datetime.fromtimestamp(to_datetime) - datetime.datetime.fromtimestamp(from_datetime)
            list_dfs = []
            for i in range(diff.days + 1):
                date = from_datetime_iso8601 + datetime.timedelta(days=i)
                download_path = f'prices_{date.year}-{date.month}-{date.day}.csv'
                download_prices(year=date.year, month=date.month, day=date.day, target_path=download_path)
                df_temp = load_prices_from_file(filepath=download_path)
                list_dfs.append(df_temp)
            df = pd.concat(list_dfs)
            return df

        # convert data to pandas dataframe
        df = pd.DataFrame(data)
        return df

# load a range of datetime values from the database with datetime format iso8601
# and return them as a pandas dataframe
def get_data_from_db_iso8601(from_datetime: str, to_datetime: str):
    # convert from_datetime to seconds since epoch and check conversion
    from_datetime_seconds = int(datetime.datetime.fromisoformat(from_datetime).timestamp())
    to_datetime_seconds = int(datetime.datetime.fromisoformat(to_datetime).timestamp())
    return get_data_from_db(from_datetime=from_datetime_seconds, to_datetime=to_datetime_seconds)


def check_stations_csv():
    with Session() as session:
        len_stations_db = len(session.query(Stations).all())
        if len_stations_db > 0:
            print('Stations already in database')
            return
        download_station(target_path='stations.csv')
        df = load_stations_from_file(filepath='stations.csv')
        add_stations(df)
