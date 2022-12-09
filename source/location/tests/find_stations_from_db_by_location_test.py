import unittest
from source.location.find_stations import find_stations_from_db_by_location
from source.data_access.functions import check_stations_csv
from source.data_access.db_model import remove_db, create_db

QUERY_OMV_DONZDORF = "omv donzdorf"
QUERY_SHELL_GÖPPINGEN = "shell göppingen"
QUERY_SHELL_RECHBERGHAUSEN = "shell rechberghausen"

QUERY_GEISLINGEN = "geislingen steige"
QUERY_PLZ_GEISLINGEN = "73312"
QUERY_BERLIN = "berlin"

class TestFindStations(unittest.TestCase):
    def test_find_stations_by_location(self):
        create_db()
        check_stations_csv()
        stations = find_stations_from_db_by_location(QUERY_OMV_DONZDORF, radius_km=0.1)
        self.assertEqual(1, len(stations))
        print(stations)
        self.assertEqual("omv", stations.iloc[0].brand)
        stations = find_stations_from_db_by_location(QUERY_SHELL_GÖPPINGEN, radius_km=0.1)
        self.assertEqual(1, len(stations))
        print(stations)
        self.assertEqual("shell", stations.iloc[0].brand)
        stations = find_stations_from_db_by_location(QUERY_SHELL_RECHBERGHAUSEN, radius_km=0.1)
        self.assertEqual(1, len(stations))
        print(stations)
        self.assertEqual("shell", stations.iloc[0].brand)
        remove_db()

    def test_find_stations_geislingen(self):
        create_db()
        check_stations_csv()
        stations = find_stations_from_db_by_location(QUERY_GEISLINGEN, radius_km=4)
        self.assertGreater(len(stations), 0)
        remove_db()

    def test_find_by_plz(self):
        create_db()
        check_stations_csv()
        stations_plz = find_stations_from_db_by_location(QUERY_PLZ_GEISLINGEN, radius_km=4)
        stations_city = find_stations_from_db_by_location(QUERY_GEISLINGEN, radius_km=4)
        self.assertEqual(len(stations_plz), len(stations_city))
        remove_db()

    def test_find_many_stations(self):
        create_db()
        check_stations_csv()
        stations = find_stations_from_db_by_location(QUERY_BERLIN, radius_km=100)
        self.assertGreater(len(stations), 0)
        remove_db()

    def test_no_query(self):
        create_db()
        stations = find_stations_from_db_by_location("", radius_km=1)
        self.assertEqual(len(stations), 0)
        remove_db()



if __name__ == '__main__':
    unittest.main()
