class ResponseHandler:
    @classmethod
    def _validate(cls, response):
        try:
            response_data = response.json()
        except Exception as e:
            print(f'[RESPONSE HANDLER] an exception occured during response validation: {str(e)}')
            return dict()

        if (message := response_data.get('retMsg')) == 'OK':
            return response_data
        else:
            print(f'[RESPONSE HANDLER] not ok response catched during response validation: {message}')
            return dict()

    @classmethod
    def handle(cls, response) -> list[str]:
        data = cls._validate(response)

        result = data.get('result', {})

        symbol = result.get('s')
        best_bid_price, best_bid_volume = result.get('b', [[None, None]])[0]
        best_ask_price, best_ask_volume = result.get('a', [[None, None]])[0]
        timestamp = result.get('ts')

        handled = [symbol, timestamp, best_bid_price, best_bid_volume, best_ask_price, best_ask_volume]

        return handled
