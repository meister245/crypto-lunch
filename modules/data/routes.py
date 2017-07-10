import sys
from utilities.helper import Util


class TradeRoutes:
    def __init__(self):
        self.util = Util()
        self.routes = {}

    def get_arbitrage_routes(self):
        """ find possible arbitrage routes based on exchange trade pairs """
        data = self.util.read_json(self.util.FILE_PAIRS)

        if len(data) == 0:
            exit('#### ERROR: No exchange trading pairs found, please generate them first')

        print("#### INFO: Looking for arbitrage routes")

        for src_exchange in data.keys():
            for trgt_exchange in data.keys():
                if src_exchange != trgt_exchange:
                    self.find_routes(data, src_exchange, trgt_exchange)

        return self.routes

    def list_trading_pairs(self, data, exchange_name):
        market_pairs = []

        for base_sym, target_syms in data[exchange_name].items():
            for sym in target_syms:
                market_pairs.append([sym, base_sym, ])

        return market_pairs

    def generate_route(self, sym_pair, tsym_pair, *args):
        if len(args) == 0:
            return {"arbitrage_sym": sym_pair[0],
                    "source_market_pair": "-".join(sym_pair),
                    "target_market_pair": "-".join(tsym_pair)}
        else:
            return {"arbitrage_sym": sym_pair[0],
                    "source_market_pair": "-".join(sym_pair),
                    args[0]: "-".join(args[1]),
                    "target_market_pair": "-".join(tsym_pair),
                    "helper_sym": args[2]}

    def find_routes(self, data, src_exchange, trgt_exchange):
        current_routes = []

        src_markets = self.list_trading_pairs(data, src_exchange)
        trgt_markets = self.list_trading_pairs(data, trgt_exchange)
        fiat = ['USD', 'EUR', 'CNY', 'CAD']

        print("#### INFO: %s - %s" % (src_exchange, trgt_exchange))
        sys.stdout.flush()

        for sym_pair in src_markets:
            for tsym_pair in trgt_markets:

                # matching market trading pairs between exchanges
                if sym_pair[0] in tsym_pair and sym_pair[1] in tsym_pair:
                    route = self.generate_route(sym_pair, tsym_pair)
                    current_routes.append(route)

                # intermediary trading pair on target exchange to bridge between market trading pairs
                if sym_pair[0] not in fiat: # exclude fiat arbitrage routes
                    if (sym_pair[0] in tsym_pair and sym_pair[1] not in tsym_pair):
                        for itsym_pair in trgt_markets:  # intermediary on target exchange
                            if itsym_pair != tsym_pair and itsym_pair != sym_pair:
                                if sym_pair[1] not in fiat: # exclude routes that include fiat transfer between exchanges
                                    self.assign_intermediaries(itsym_pair, "source_intermediary", sym_pair, tsym_pair, current_routes)

                if sym_pair[0] not in fiat:  # exclude fiat arbitrage routes
                    if (sym_pair[0] in tsym_pair and sym_pair[1] not in tsym_pair):
                        for isym_pair in src_markets:  # intermediary on source exchange
                            if isym_pair != sym_pair and isym_pair != tsym_pair:
                                if tsym_pair[0] not in fiat or tsym_pair[1] not in fiat: # exclude routes that include fiat transfer between exchanges
                                    self.assign_intermediaries(isym_pair, "target_intermediary", sym_pair, tsym_pair, current_routes)

        if len(current_routes) != 0:
            exchange_pair = src_exchange + "-" + trgt_exchange
            self.routes[exchange_pair] = current_routes

    def assign_intermediaries(self, inter_pair, inter_type, sym_pair, tsym_pair, current_routes):
        if inter_pair[0] in sym_pair and inter_pair[0] not in tsym_pair and inter_pair[1] not in sym_pair and inter_pair[1] in tsym_pair:
            current_routes.append(self.generate_route(sym_pair, tsym_pair, inter_type, inter_pair, self.get_helper_sym(sym_pair, tsym_pair)))
        if inter_pair[0] not in sym_pair and inter_pair[0] in tsym_pair and inter_pair[1] in sym_pair and inter_pair[1] not in tsym_pair:
            current_routes.append(self.generate_route(sym_pair, tsym_pair, inter_type, inter_pair, self.get_helper_sym(sym_pair, tsym_pair)))

    def get_helper_sym(self, source_pair, target_pair):
        for sym in target_pair:
            if sym not in source_pair:
                return sym
