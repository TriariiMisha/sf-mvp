import re


DURATION_PATTERN = re.compile('\d+\.*\d*[d|h|m|s]')
REST_URL = 'https://api.bybit.com/v5/market/orderbook?category=spot&limit=1'
RPS_LIMIT = 120
