import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil import tz


# convert dataframe from auto format to seconds since epoch
def convert_df_to_epoch_seconds_utc(df: pd.DataFrame, column: str):
    series = pd.to_datetime(df[column], infer_datetime_format=True, utc=True)
    timedelta = series - datetime(1970, 1, 1, tzinfo=tz.gettz('UTC'))
    timedelta = timedelta / np.timedelta64(1, 's')
    timedelta = timedelta.astype('int64')
    series = timedelta
    return series

# convert dataframe from seconds since epoch to iso8601 format
def convert_df_from_epoch_to_iso8601_tz(df: pd.DataFrame, column: str, timezone: tz.tzfile = tz.gettz('UTC')):
    df[column] = pd.to_datetime(df[column], unit='s', utc=True)
    df[column] = df[column].dt.tz_convert(timezone)
    return df