import unittest
from data_access.tests.TestCheckStations import TestCheckStations
from data_access.tests.TestDownloadOfPrices import TestGetDataFromDb
from data_access.tests.TestGetMVPStationInfo import TestGetMVPStationInfo
from data_access.tests.TestGetStationsByCoords import TestGetStationsByCoords
from datetime_conversion.tests.test_datetime_conversion import TestDatetimeConversion
from download_files.tests.test_download_files import TestDownloadFiles
from location.tests.find_coordinates_test import TestFindCoordinates
from location.tests.find_stations_from_db_by_location_test import TestFindStations


if __name__ == '__main__':
    unittest.main()