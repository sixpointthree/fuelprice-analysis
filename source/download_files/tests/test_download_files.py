import unittest
import os
from source.download_files.downloader import download_prices, download_stations, download_station

FILE_NAME = "test.csv"

class TestDownloadFiles(unittest.TestCase):
    def test_download_prices(self):
        download_prices(2019, 1, 1, FILE_NAME)
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        else:
            self.fail(f"File {FILE_NAME} not found")

    def test_download_prices_invalid_date(self):
        download_prices(2006, 1, 1, FILE_NAME)
        if os.path.exists(FILE_NAME):
            self.fail(f"File {FILE_NAME} found")

    def test_download_stations(self):
        download_stations(2020, 1, 1, FILE_NAME)
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        else:
            self.fail(f"File {FILE_NAME} not found")

    def test_download_stations_invalid_date(self):
        download_stations(2006, 1, 1, FILE_NAME)
        if os.path.exists(FILE_NAME):
            self.fail(f"File {FILE_NAME} found")

    def test_download_the_station(self):
        download_station(target_path=FILE_NAME)
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        else:
            self.fail(f"File {FILE_NAME} not found")


if __name__ == '__main__':
    unittest.main()
