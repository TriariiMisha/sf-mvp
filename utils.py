from math import log
from datetime import datetime


def get_timestamp(dt: datetime) -> int:
    timestamp = int(dt.timestamp())

    return timestamp


def get_time_to_sleep(limit_per_second, tickers_number) -> tuple:
    requests_per_second = limit_per_second / (tickers_number + (1 + log(tickers_number)))
    seconds_to_wait = 1 / requests_per_second
    real_requests_per_second = int(1 / seconds_to_wait * tickers_number)

    return seconds_to_wait, real_requests_per_second
