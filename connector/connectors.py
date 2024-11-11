from abc import ABC, abstractmethod
from requests import Session, Response
from consts import REST_URL as URL


class Connector(ABC):
    @abstractmethod
    def get(self, ticker):
        pass


class HTTPConnector(Connector):
    def __init__(self, headers):
        session = Session()
        session.headers.update(headers)

        self.session = session

        print('[CONNECTOR] new session established...')

    def get(self, ticker) -> Response:
        url = f'{URL}&symbol={ticker}'
        response = self.session.get(url)

        return response
