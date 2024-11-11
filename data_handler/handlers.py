import pickle

from abc import ABC, abstractmethod
from utils import get_timestamp
from datetime import datetime


class DataHandler(ABC):
    def __init__(self, batch_size: int):
        self.items = []
        self.batch_size = batch_size

    def add_items(self, new_items: list):
        self.items.append(new_items)

    def _check_readiness(self):
        return len(self.items) >= self.batch_size

    @abstractmethod
    def write(self):
        pass


class PickleDataHandler(DataHandler):
    def write(self, final=False):
        timestamp = get_timestamp(datetime.now())
        filepath = f'output/result{timestamp}.pickle'

        if not final:
            if self._check_readiness():
                items_to_write = self.items[:self.batch_size]
                self.items = self.items[self.batch_size:]

                with open(filepath, 'wb') as file:
                    pickle.dump(items_to_write, file)

                print(f'[DATA HANDLER] {self.batch_size} items saved to file {filepath}...')
        else:
            with open(filepath, 'wb') as file:
                pickle.dump(self.items, file)

            print(f'[DATA HANDLER] items are finally saved to file {filepath}...')


class PostgresDataHandler(DataHandler):
    def write(self, final=False):
        pass