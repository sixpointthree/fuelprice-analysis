import unittest
from source.data_access.tests.test_check_stations import TestCheckStations
from source.data_access.tests.test_download_of_prices import TestGetDataFromDb
from source.data_access.tests.test_get_mvp_station_info import TestGetMVPStationInfo
from source.data_access.tests.test_get_stations_by_coords import TestGetStationsByCoords
from source.datetime_conversion.tests.test_datetime_conversion import TestDatetimeConversion
from source.download_files.tests.test_download_files import TestDownloadFiles
from source.location.tests.find_coordinates_test import TestFindCoordinates
from source.location.tests.find_stations_from_db_by_location_test import TestFindStations


if __name__ == '__main__':
    unittest.main()