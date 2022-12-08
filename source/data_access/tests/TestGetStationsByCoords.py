import unittest
from source.data_access.functions import get_stations_by_coords

class TestGetStationsByCoords(unittest.TestCase):
    def test_get_stations_by_coords(self):
        stations = get_stations_by_coords(lat=48.6858127, lon=9.7896475, radius_km=50)
        print(stations)


if __name__ == '__main__':
    unittest.main()
