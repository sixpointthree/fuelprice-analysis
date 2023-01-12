import unittest
from source.data_access.functions import get_stations_by_coords, check_stations_csv
from source.data_access.db_model import remove_db, create_db

class TestGetStationsByCoords(unittest.TestCase):
    def test_get_stations_by_coords(self):
        create_db()
        check_stations_csv()
        stations = get_stations_by_coords(lat=48.6858127, lon=9.7896475, radius_km=1)
        print(stations)
        remove_db()



if __name__ == '__main__':
    unittest.main()
