import unittest
from source.data_access.functions import check_stations_csv
from source.data_access.db_model import remove_db


# test check_stations.csv
class TestCheckStations(unittest.TestCase):
    def test_check_stations(self):
        check_stations_csv()
        remove_db()
        # delete all db files in this folder


if __name__ == '__main__':
    unittest.main()
