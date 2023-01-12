import unittest
from source.location.find_coordinates import find_coors_by_text

QUERY_OMV_DONZDORF = "omv donzdorf"
QUERY_SHELL_GÖPPINGEN = "shell göppingen"
QUERY_SHELL_RECHBERGHAUSEN = "shell rechberghausen"


class TestFindCoordinates(unittest.TestCase):
    def test_find_coors_by_text(self):
        lat, lon = find_coors_by_text(QUERY_OMV_DONZDORF)
        self.assertAlmostEqual(48.6858127, float(lat), places=5)
        self.assertAlmostEqual(9.7896475, float(lon), places=5)
        lat, lon = find_coors_by_text(QUERY_SHELL_GÖPPINGEN)
        self.assertAlmostEqual(48.6956320, float(lat), places=5)
        self.assertAlmostEqual(9.6651296, float(lon), places=5)
        lat, lon = find_coors_by_text(QUERY_SHELL_RECHBERGHAUSEN)
        self.assertAlmostEqual(48.7256682, float(lat), places=5)
        self.assertAlmostEqual(9.6423544, float(lon), places=5)

    def test_invalid_input(self):
        with self.assertRaises(AttributeError):
            find_coors_by_text("")


if __name__ == '__main__':
    unittest.main()
