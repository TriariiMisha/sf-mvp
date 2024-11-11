from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor


class Multiprocessor(ABC):
    def __init__(self, connection, response_handler, data_handler):
        self.connection = connection
        self.response_handler = response_handler
        self.data_handler = data_handler

    def run(self, ticker):
        result = self.connection.get(ticker)
        result_handled = self.response_handler.handle(result)

        self.data_handler.add_items(result_handled)

    @abstractmethod
    def parallel_run(self, tickers: list):
        pass


class ThreadMultiprocessor(Multiprocessor):
    def parallel_run(self, tickers: list):
        max_workers = len(tickers)  # infer max workers from tickers count

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(lambda ticker: self.run(ticker), tickers)

        self.data_handler.write()
