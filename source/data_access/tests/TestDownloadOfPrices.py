import unittest

import dateutil.tz

from source.data_access.functions import get_prices, get_prices_by_date_tz
from datetime import datetime

TIMESTAMP_2020_01_01_BEGIN = datetime(2020, 1, 1, 0, 0, 0)
TIMESTAMP_2020_01_01_END = datetime(2020, 1, 1, 23, 59, 59)
TIMESTAMP_2020_01_03_END = datetime(2020, 1, 3, 23, 59, 59)

UUID_OMV_DONZDORF = "16f07bfd-0bde-4126-a393-ea8a7d053283"
UUID_ARAL_GOEPPINGEN = "77c4cc3c-ae11-43c4-85cc-5c147409b46f"
UUID_SHELL_GOEPPINGEN = "c13f60cb-7e1c-40a8-b05a-157fd571b3fa"

KNOWN_RECORD_CNT_2020_01_01 = 207897
KNOWN_RECORD_CNT_2020_01_01_2020_01_03 = 746939
KNOWN_RECORD_CNT_MVP_STAT_2020_01_01_2020_01_03 = 135

# test get_data_from_db
class TestGetDataFromDb(unittest.TestCase):
    def test_one_day_get_data_from_db(self):
        self.assertTrue(len(get_prices(from_datetime=int(TIMESTAMP_2020_01_01_BEGIN.timestamp()),
                                       to_datetime=int(TIMESTAMP_2020_01_01_END.timestamp())))
                        == KNOWN_RECORD_CNT_2020_01_01)

    def test_multiple_days_get_data_from_db(self):
        self.assertTrue(len(get_prices(from_datetime=int(TIMESTAMP_2020_01_01_BEGIN.timestamp()),
                                       to_datetime=int(TIMESTAMP_2020_01_03_END.timestamp())))
                        == KNOWN_RECORD_CNT_2020_01_01_2020_01_03)

    def test_get_data_from_db_mvp_stations(self):
        self.assertTrue(len(get_prices(from_datetime=int(TIMESTAMP_2020_01_01_BEGIN.timestamp()),
                                       to_datetime=int(TIMESTAMP_2020_01_03_END.timestamp()),
                                       station_uuids=[UUID_OMV_DONZDORF, UUID_ARAL_GOEPPINGEN,
                                                            UUID_SHELL_GOEPPINGEN]))
                        == KNOWN_RECORD_CNT_MVP_STAT_2020_01_01_2020_01_03)

    def test_get_prices_high_level_func(self):
        prices = get_prices_by_date_tz(from_date=TIMESTAMP_2020_01_01_BEGIN,
                                       to_date=TIMESTAMP_2020_01_03_END,
                                       station_uuids=[UUID_OMV_DONZDORF, UUID_ARAL_GOEPPINGEN,
                                                            UUID_SHELL_GOEPPINGEN],
                                                  tz=dateutil.tz.gettz("Europe/Berlin"))
        self.assertTrue(len(prices)
                        == KNOWN_RECORD_CNT_MVP_STAT_2020_01_01_2020_01_03)
        self.assertTrue(prices['timestamp'].dt.tz == dateutil.tz.gettz("Europe/Berlin"))


if __name__ == '__main__':
    unittest.main()
