import sys
from time import time
from utilities.helper import Util
from modules.api.cryptocompare_api import CryptoCompareAPI


class Arbitrage:
    def __init__(self):
        self.util = Util()
        self.api = CryptoCompareAPI()

        self.valid_routes = {}
        self.profit_routes = {}
        self.price_cache = {}

    def start_service(self, filter='all', *args):
        # assign price to routes, filter routes that contain stale prices
        self.routes = self.util.read_json(self.util.FILE_ROUTES)
        self.profit_margin = self.util.read_json(self.util.CONFIG)['profit_margin']

        print("#### INFO: Calculating profitable arbitrage routes")
        sys.stdout.flush()

        for cx_pair, ar_routes in self.routes.items():
            cx_source, cx_target = cx_pair.split('-')

            if filter == 'source':
                if cx_source.lower() in args[0]:
                    print("#### INFO: Processing '%s'" % cx_pair)
                    sys.stdout.flush()

                    self.valid_routes[cx_pair] = []
                    for idx, route in enumerate(ar_routes):
                        try:
                            priced_route = self.assign_prices_to_route(route, idx, cx_pair)
                            self.valid_routes[cx_pair].append(priced_route)
                        except ValueError:
                            pass

            if filter == 'target':
                if cx_target.lower() in args[0]:
                    print("#### INFO: Processing '%s'" % cx_pair)
                    sys.stdout.flush()

                    self.valid_routes[cx_pair] = []
                    for idx, route in enumerate(ar_routes):
                        try:
                            priced_route = self.assign_prices_to_route(route, idx, cx_pair)
                            self.valid_routes[cx_pair].append(priced_route)
                        except ValueError:
                            pass

            if filter == 'all':
                print("#### INFO: Processing '%s'" % cx_pair)
                sys.stdout.flush()

                self.valid_routes[cx_pair] = []
                for idx, route in enumerate(ar_routes):
                    try:
                        priced_route = self.assign_prices_to_route(route, idx, cx_pair)
                        self.valid_routes[cx_pair].append(priced_route)
                    except ValueError:
                        pass

        # calculate profitable routes
        for cx_pair, ar_routes in self.valid_routes.items():
            self.profit_routes[cx_pair] = []
            for route in ar_routes:
                self.calculate_profitability(route, cx_pair)
            if len(self.profit_routes[cx_pair]) == 0:
                del self.profit_routes[cx_pair]

        # write profitable routes to file
        self.util.write_json_to_file(self.profit_routes, self.util.FILE_PROFIT)
        print("#### INFO: Profitable arbitrage routes written to file")

        return

    def assign_prices_to_route(self, route, idx, cx_pair):
        source_cx, target_cx = cx_pair.split('-')

        src_price = self.get_price_for_market_pair(route['source_market_pair'], source_cx)
        self.routes[cx_pair][idx]['source_market_price'] = src_price

        if 'source_intermediary' in route:
            is_price = self.get_price_for_market_pair(route['source_intermediary'], source_cx)
            self.routes[cx_pair][idx]['source_intermediary_price'] = is_price

        if 'target_intermediary' in route:
            it_price = self.get_price_for_market_pair(route['target_intermediary'], target_cx)
            self.routes[cx_pair][idx]['target_intermediary_price'] = it_price

        target_price = self.get_price_for_market_pair(route['target_market_pair'], target_cx)
        self.routes[cx_pair][idx]['target_market_price'] = target_price

        return self.routes[cx_pair][idx]

    def get_price_for_market_pair(self, pair, cx):
        """ use price caching to require less API requests """
        fsym, tsym = pair.split('-')
        req_params = {"fsyms": fsym, "tsyms": tsym, "e": cx}

        if not cx in self.price_cache.keys():
            self.price_cache[cx] = {}

        if pair in self.price_cache[cx].keys():
            price = self.price_cache[cx][pair]['price']
            last_update = self.price_cache[cx][pair]['lastupdate']

        else:
            try:
                req_data = self.api.get_price_multifull(req_params)['RAW'][fsym][tsym]
                price = req_data['PRICE']
                last_update = req_data['LASTUPDATE']
                self.price_cache[cx][pair] = {"price": price, "lastupdate": last_update}
            except KeyError:
                raise ValueError

        self.check_stale_data(last_update)

        return price

    def calculate_profitability(self, route, cx_pair):
        result = float(route['source_market_price']) * 100.0

        if len(route.keys()) == 5:
            result = result / float(route['target_market_price'])

            if result > 100.0 and (result - 100.0) > float(self.profit_margin):
                self.store_profitable_route(route, result, cx_pair)

        elif len(route.keys()) == 8:
            if 'target_intermediary_price' in route:
                result = self.calc_inter(result, route, route['target_intermediary'],
                                         route['target_intermediary_price'])
            elif 'source_intermediary_price' in route:
                result = self.calc_inter(result, route, route['source_intermediary'],
                                         route['source_intermediary_price'])

            if result > 100.0 and (result - 100.0) > float(self.profit_margin):
                self.store_profitable_route(route, result, cx_pair)

    def store_profitable_route(self, route, result, cx_pair):
        route['profit_margin'] = str(float(result) - 100.0)[:5]
        self.profit_routes[cx_pair].append(route)

    def calc_inter(self, result, route, inter_market, inter_price):
        """ if route has intermediary price, do calculation """
        hsym = route['helper_sym']
        inter_sym, inter_tsym = inter_market.split('-')
        target_sym, target_tsym = route['target_market_pair'].split('-')

        if inter_sym == hsym:
            result = float(result) / float(inter_price)
        elif inter_tsym == hsym:
            result = float(result) * float(inter_price)

        if target_tsym == hsym:
            result = float(result) / float(route['target_market_price'])
        elif target_sym == hsym:
            result = float(result) * float(route['target_market_price'])

        return result

    def check_stale_data(self, lastupdate):
        if lastupdate + 60 > time():
            return
        else:
            raise ValueError
