import requests

URL_COIN = 'https://www.cryptocompare.com/api/data/coinlist/'
URL_PRICE = 'https://min-api.cryptocompare.com/data/'


class CryptoCompareAPI:
    def __init__(self):
        pass

    def api_query(self, method, **params):

        def fsym(method):
            return 'fsym' if method == 'price' else 'fsyms'

        if method == 'coinlist':
            return requests.get(URL_COIN)

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
