from .find_coordinates import find_coors_by_text




def find_stations_from_db_by_location(query: str, radius_km: int) -> list:
    """
    Find stations from database by location.
    :param query: location query
    :param radius_km: radius in km
    :return: list of stations
    """
    lat, lon = find_coors_by_text(query)
    stations = get_stations_by_coords(lat, lon, radius_km)
    return stations