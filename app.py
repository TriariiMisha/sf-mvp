import os
from datetime import datetime
from time import sleep

from args_parser.parser import parser
from args_parser.args import Duration
from connector.connectors import HTTPConnector
from response_handler.handlers import ResponseHandler
from data_handler.handlers import PickleDataHandler
from multiprocess.processor import ThreadMultiprocessor
from utils import get_timestamp, get_time_to_sleep
from consts import RPS_LIMIT


class MVP:
    def __init__(self, tickers_file: str, duration_string: str, batch_size: int):
        # process tickers
        if not os.path.isfile(tickers_file):
            raise ValueError(f'{tickers_file} is not a file!')

        with open(tickers_file, 'r') as file:
            tickers = file.read().split()

        self.tickers = tickers

        # process duration
        duration = Duration(duration_string)
        self.seconds = duration.to_seconds()

        # process batch_size
        if not isinstance(batch_size, int):
            raise ValueError(f'{batch_size} argument must be of time integer!')

        self.batch_size = batch_size

        print('[MVP] process successfully initialized with parameters:')

        print(f'\t tickers: {", ".join(self.tickers)}')
        print(f'\t duration: {self.seconds} seconds')
        print(f'\t batch_size: {self.batch_size} records')

    @classmethod
    def from_args(cls):
        args = parser.parse_args()

        args_dict = {
            "tickers_file": args.tickers_file,
            "duration_string": args.duration,
            "batch_size": args.batch_size,
        }

        instance = cls(**args_dict)

        return instance


    def run(self):
        # get connector
        conn = HTTPConnector(headers=dict())

        # get data handler
        data_handler = PickleDataHandler(self.batch_size)

        # map to multiprocess and run
        multiprocess = ThreadMultiprocessor(
            connection=conn, response_handler=ResponseHandler, data_handler=data_handler
        )

        # run
        ts_current = get_timestamp(datetime.now())
        ts_to_finish = ts_current + self.seconds

        seconds_to_sleep, real_rps = get_time_to_sleep(RPS_LIMIT, len(self.tickers))

        print(f'[MVP] due to rps limit {RPS_LIMIT} sleep interval is {seconds_to_sleep:.2f} (real rps is {real_rps})')

        while ts_to_finish > ts_current:
            multiprocess.parallel_run(self.tickers)
            ts_current = get_timestamp(datetime.now())
            sleep(seconds_to_sleep)
        else:
            data_handler.write(final=True)
