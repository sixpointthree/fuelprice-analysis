import unittest
from source.data_access.functions import get_prices
from datetime import datetime

TIMESTAMP_2020_01_01_BEGIN = int(datetime(2020, 1, 1, 0, 0, 0).timestamp())
TIMESTAMP_2020_01_01_END = int(datetime(2020, 1, 1, 23, 59, 59).timestamp())
TIMESTAMP_2020_01_03_END = int(datetime(2020, 1, 3, 23, 59, 59).timestamp())

UUID_OMV_DONZDORF = "16f07bfd-0bde-4126-a393-ea8a7d053283"
UUID_ARAL_GOEPPINGEN = "77c4cc3c-ae11-43c4-85cc-5c147409b46f"
UUID_SHELL_GOEPPINGEN = "c13f60cb-7e1c-40a8-b05a-157fd571b3fa"

KNOWN_RECORD_CNT_2020_01_01 = 207897
KNOWN_RECORD_CNT_2020_01_01_2020_01_03 = 746939
KNOWN_RECORD_CNT_MVP_STAT_2020_01_01_2020_01_03 = 135

# test get_data_from_db
class TestGetDataFromDb(unittest.TestCase):
    def test_one_day_get_data_from_db(self):
        self.assertTrue(len(get_prices(from_datetime=TIMESTAMP_2020_01_01_BEGIN,
                                       to_datetime=TIMESTAMP_2020_01_01_END))
                        == KNOWN_RECORD_CNT_2020_01_01)

    def test_multiple_days_get_data_from_db(self):
        self.assertTrue(len(get_prices(from_datetime=TIMESTAMP_2020_01_01_BEGIN,
                                       to_datetime=TIMESTAMP_2020_01_03_END))
                        == KNOWN_RECORD_CNT_2020_01_01_2020_01_03)

    def test_get_data_from_db_mvp_stations(self):
        self.assertTrue(len(get_prices(from_datetime=TIMESTAMP_2020_01_01_BEGIN,
                                       to_datetime=TIMESTAMP_2020_01_03_END,
                                       station_uuids=[UUID_OMV_DONZDORF, UUID_ARAL_GOEPPINGEN,
                                                            UUID_SHELL_GOEPPINGEN]))
                        == KNOWN_RECORD_CNT_MVP_STAT_2020_01_01_2020_01_03)

if __name__ == '__main__':
    unittest.main()
