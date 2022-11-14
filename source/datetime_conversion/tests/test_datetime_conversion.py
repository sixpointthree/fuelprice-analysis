import unittest
import pandas as pd
from dateutil import tz

from source.datetime_conversion.functions import convert_df_to_epoch_seconds_utc, convert_df_from_epoch_to_iso8601_tz


# function to convert datetime64 to iso8601 string
def to_string(x):
    return x.strftime("%Y-%m-%d %H:%M:%S%z")


class TestDatetimeConversion(unittest.TestCase):
    def test_convert_df_to_epoch_seconds_utc(self):
        df = pd.DataFrame({'date': ['2019-11-10 00:00:00+01', '2022-11-10 00:00:00+01', '2019-10-01 00:00:00+02']})
        df = convert_df_to_epoch_seconds_utc(df, 'date')
        self.assertEqual(df['date'][0], 1573340400)
        self.assertEqual(df['date'][1], 1668034800)
        self.assertEqual(df['date'][2], 1569880800)

    def test_convert_from_epoch_to_iso8601_tz(self):
        df = pd.DataFrame({'date': [1573340400, 1668034800, 1569880800]})
        df = convert_df_from_epoch_to_iso8601_tz(df, 'date', tz.gettz('Europe/Berlin'))
        print(df.head())
        print(df.dtypes)
        self.assertEqual(to_string(df['date'][0]), '2019-11-10 00:00:00+0100')
        self.assertEqual(to_string(df['date'][1]), '2022-11-10 00:00:00+0100')
        self.assertEqual(to_string(df['date'][2]), '2019-10-01 00:00:00+0200')


if __name__ == '__main__':
    unittest.main()
