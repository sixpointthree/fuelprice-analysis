import unittest
import os
from source.download_files.downloader import download_file

FILE_NAME = "test.csv"

class TestDownloadFiles(unittest.TestCase):
    def test_download_file(self):
        download_file(2019, 1, 1, FILE_NAME)
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        else:
            self.fail(f"File {FILE_NAME} not found")

    def test_download_file_invalid_date(self):
        download_file(2006, 1, 1, FILE_NAME)
        if os.path.exists(FILE_NAME):
            self.fail(f"File {FILE_NAME} found")


if __name__ == '__main__':
    unittest.main()
