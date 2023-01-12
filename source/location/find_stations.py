import pandas as pd

from .find_coordinates import find_coors_by_text
from source.data_access.functions import get_stations_by_coords

def find_stations_from_db_by_location(query: str, radius_km: float) -> pd.DataFrame:
    """
    Find stations from database by location.
    :param query: location query
    :param radius_km: radius in km
    :return: list of stations
    """
    try:
        lat, lon = find_coors_by_text(query)
    except AttributeError as e:
        print(e)
        return pd.DataFrame()
    except RuntimeError as e:
        print(e)
        return pd.DataFrame()
    try:
        stations = get_stations_by_coords(lat, lon, radius_km)
    except ValueError as e:
        print(e)
        return pd.DataFrame()
    return stations