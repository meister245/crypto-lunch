import requests


class CryptoCompareAPI(object):
    url_base = 'https://min-api.cryptocompare.com/data'

    @classmethod
    def api_query(cls, method, api_endpoint, **kwargs):
        return requests.request(method, cls.url_base + api_endpoint, **kwargs)

    @classmethod
    def get_exchange_pairs(cls, method='GET', **kwargs):
        return cls.api_query(method=method, api_endpoint='/all/exchanges', **kwargs).json()

    @classmethod
    def get_price_multi_full(cls, method='GET', **kwargs):
        return cls.api_query(method=method, api_endpoint='/pricemultifull', **kwargs).json()
