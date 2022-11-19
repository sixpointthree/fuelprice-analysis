import unittest
from source.data_access.functions import get_station_info_uuid, check_stations_csv

UUID_OMV_DONZDORF = "16f07bfd-0bde-4126-a393-ea8a7d053283"
UUID_ARAL_GOEPPINGEN = "77c4cc3c-ae11-43c4-85cc-5c147409b46f"
UUID_SHELL_GOEPPINGEN = "c13f60cb-7e1c-40a8-b05a-157fd571b3fa"

class TestGetMVPStationInfo(unittest.TestCase):
    def test_get_station_info_uuid(self):
        check_stations_csv()
        info = get_station_info_uuid(UUID_OMV_DONZDORF)
        self.assertEqual("omv", info.brand)
        info = get_station_info_uuid(UUID_ARAL_GOEPPINGEN)
        self.assertEqual("aral", info.brand)
        info = get_station_info_uuid(UUID_SHELL_GOEPPINGEN)
        self.assertEqual("shell", info.brand)


if __name__ == '__main__':
    unittest.main()
