import time

from lib.cryptocompare import CryptoCompareAPI

import cachetools.func


class ArbitrageController(object):
    api = CryptoCompareAPI()

    @classmethod
    def run_arbitrage(cls, routes, profit_margin=1.0):
        routes_priced = cls.get_routes_priced(routes)
        routes_profit = cls.get_routes_profit(routes_priced, profit_margin)

        return routes_profit

    @classmethod
    def get_routes_priced(cls, cx_routes):
        priced_routes = {}

        for cx_pair, routes in cx_routes.items():
            p_routes = []

            for route in routes:
                try:
                    p_routes.append(cls.get_priced_route(route, cx_pair))
                    print(f'retrieved prices for {len(p_routes)} routes - {cx_pair}\r', end='')

                except ValueError:
                    pass

            priced_routes.update({cx_pair: p_routes})
            print(f'retrieved prices for {len(p_routes)} routes - {cx_pair}')

        return priced_routes

    @classmethod
    def get_routes_profit(cls, routes_priced, profit_margin=1.0):
        profit_routes = {}

        for cx_pair, routes in routes_priced.items():
            p_routes = []

            for route in routes:
                for p_route in cls.calculate_route_profit(route, profit_margin):
                    p_routes.append(p_route)
                    print(f'calculated {len(p_routes)} profitable routes for {cx_pair}\r', end='')

            profit_routes.update({cx_pair: p_routes})
            print(f'calculated {len(p_routes)} profitable routes for {cx_pair}')

        return profit_routes

    @classmethod
    def get_priced_route(cls, route, cx_pair):
        source_cx, target_cx = cx_pair.split('-')

        route['source_market_price'] = cls.get_market_pair_price(route['source_market_pair'], source_cx)

        if 'source_intermediary' in route:
            route['source_intermediary_price'] = cls.get_market_pair_price(route['source_intermediary'], source_cx)

        if 'target_intermediary' in route:
            route['target_intermediary_price'] = cls.get_market_pair_price(route['target_intermediary'], target_cx)

        route['target_market_price'] = cls.get_market_pair_price(route['target_market_pair'], target_cx)

        return route

    @classmethod
    @cachetools.func.ttl_cache(ttl=60)
    def get_market_pair_price(cls, pair, cx_name):
        tsym, fsym = pair.split('-')
        response = cls.api.get_price_multifull({"fsyms": fsym, "tsyms": tsym, "e": cx_name})

        if not response['RAW'][fsym][tsym]['LASTUPDATE'] + 3600 > int(time.time()):
            raise ValueError('stale market')

        return response['RAW'][fsym][tsym]['PRICE']

    @classmethod
    def calculate_route_profit(cls, route, profit_margin=1.0):
        result = float(route['source_market_price']) * 100.0
        target_sym, target_tsym = route['target_market_pair'].split('-')

        if 'target_intermediary_price' in route:
            result = cls.calculate_intermediary(result, route, i_type='target')

        elif 'source_intermediary_price' in route:
            result = cls.calculate_intermediary(result, route, i_type='source')

        if target_tsym == route['helper_sym']:
            result = float(result) / float(route['target_market_price'])

        elif target_sym == route['helper_sym']:
            result = float(result) * float(route['target_market_price'])

        if result > 100.0 and (result - 100.0) > profit_margin:
            route['profit_margin'] = float(result - 100.0)
            yield route

    @staticmethod
    def calculate_intermediary(result, route, i_type):
        inter_sym, inter_tsym = route[f'{i_type}_intermediary'].split('-')

        if inter_sym == route['helper_sym']:
            result = float(result) / float(route[f'{i_type}_intermediary_price'])

        elif inter_tsym == route['helper_sym']:
            result = float(result) * float(route[f'{i_type}_intermediary_price'])

        return result
