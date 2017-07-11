import requests

URL_COIN = 'https://www.cryptocompare.com/api/data/coinlist/'
URL_EXCHANGES = 'https://min-api.cryptocompare.com/data/all/exchanges'
URL_PRICE = 'https://min-api.cryptocompare.com/data/'
URL_SNAPSHOT = 'https://www.cryptocompare.com/api/data/'


class CryptoCompareAPI:
    def __init__(self):
        pass

    def api_query(self, method, **params):
        url_params = []

        if method in ['coinlist']:
            return requests.get(URL_COIN)

        if method in ['coinsnapshot']:
            for k, v in params.items():
                url_params.append(k + "=" + v)

            return requests.get(URL_SNAPSHOT + method + '/?' + "&".join(url_params))

        if method in ['pricemultifull']:
            for k, v in params.items():
                if k in ['fsyms', 'tsyms', 'e']:
                    url_params.append(k + "=" + v)

            return requests.get(URL_PRICE + method + '?' + "&".join(url_params))

        if method in ['exchanges']:
            return requests.get(URL_EXCHANGES)

    def get_coinlist(self):
        return self.api_query('coinlist').json()

    def get_exchange_pairs(self):
        return self.api_query('exchanges').json()

    def get_price(self, params):
        return self.api_query('price', **params).json()

    def get_price_multi(self, params):
        return self.api_query('pricemulti', **params).json()

    def get_price_multifull(self, params):
        return self.api_query('pricemultifull', **params).json()

    def get_coin_snapshot(self, params):
        return self.api_query('coinsnapshot', **params).json()
