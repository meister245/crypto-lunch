import requests

URL_COIN = 'https://www.cryptocompare.com/api/json/coinlist/'
URL_PRICE = 'https://min-api.cryptocompare.com/json/'
URL_SNAPSHOT = 'https://www.cryptocompare.com/api/data/'


class CryptoCompareAPI:
    def __init__(self):
        pass

    def api_query(self, method, **params):

        def fsym(method):
            return 'fsym' if method == 'price' else 'fsyms'

        if method in ['coinlist']:
            return requests.get(URL_COIN)

        if method in ['coinsnapshot']:
            url_params = []

            for k, v in params.items():
                url_params.append(k + "=" + v)

            return requests.get(URL_SNAPSHOT + method + '?' + "&".join(url_params))

        if method in ['price', 'pricemulti', 'pricemultifull']:
            url_params = []

            for k, v in params.items():
                if k in [fsym(method), 'tsyms']:
                    url_params.append(k + "=" + ",".join(v))
                else:
                    url_params.append(k + "=" + v)

            return requests.get(URL_PRICE + method + '?' + "&".join(url_params))

    def get_coinlist(self):
        return self.api_query('coinlist').json()

    def get_price(self, params):
        return self.api_query('price', **params).json()

    def get_price_multi(self, params):
        return self.api_query('pricemulti', **params).json()

    def get_price_multi_full(self, params):
        return self.api_query('pricemultifull', **params).json()

    def get_coin_snapshot(self, params):
        return self.api_query('coinsnapshot', **params).json()
