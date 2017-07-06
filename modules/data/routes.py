from utilities.helper import Util


class TradeRoutes:
    def __init__(self):
        self.util = Util()
        self.routes = {}

    def get_arbitrage_routes(self):
        """ find possible arbitrage routes based on exchange trade pairs """
        data = self.util.read_json(self.util.FILE_CXPAIRS)

        for src_exchange in data.keys():
            for trgt_exchange in data.keys():
                if src_exchange != trgt_exchange:
                    self.find_routes(data, src_exchange, trgt_exchange)

        return self.routes

    def list_trading_pairs(self, data, exchange_name):
        market_pairs = []

        for base_sym, target_syms in data[exchange_name].items():
            for sym in target_syms:
                market_pairs.append([base_sym, sym])

        return market_pairs

    def generate_route(self, sym_pair, tsym_pair, *args):
        if len(args) == 0:
            return {"arbitrage_sym": sym_pair[1],
                    "source_market_pair": "-".join(sym_pair),
                    "target_market_pair": "-".join(tsym_pair)}
        else:
            return {"arbitrage_sym": sym_pair[1],
                    "source_market_pair": "-".join(sym_pair),
                    args[0]: "-".join(args[1]),
                    "target_market_pair": "-".join(tsym_pair),
                    "helper_sym": args[2]}

    def find_routes(self, data, src_exchange, trgt_exchange):
        current_routes = []

        src_markets = self.list_trading_pairs(data, src_exchange)
        trgt_markets = self.list_trading_pairs(data, trgt_exchange)

        for sym_pair in src_markets:
            for tsym_pair in trgt_markets:

                # matching market trading pairs between exchanges
                if sym_pair[0] in tsym_pair and sym_pair[1] in tsym_pair:
                    route = self.generate_route(sym_pair, tsym_pair)
                    current_routes.append(route)

                # intermediary trading pair on target exchange to bridge between market trading pairs
                if (sym_pair[0] not in tsym_pair and sym_pair[1] in tsym_pair):
                    for itsym_pair in trgt_markets:  # intermediary on target exchange
                        if itsym_pair != tsym_pair and itsym_pair != sym_pair:
                            if itsym_pair[0] in sym_pair and itsym_pair[0] not in tsym_pair and itsym_pair[1] not in sym_pair and itsym_pair[1] in tsym_pair:
                                current_routes.append(self.generate_route(sym_pair, tsym_pair, "target_intermediary", itsym_pair,itsym_pair[0]))
                            if itsym_pair[0] not in sym_pair and itsym_pair[0] in tsym_pair and itsym_pair[1] in sym_pair and itsym_pair[1] not in tsym_pair:
                                current_routes.append(self.generate_route(sym_pair, tsym_pair, "target_intermediary", itsym_pair,itsym_pair[0]))

                if (sym_pair[0] not in tsym_pair and sym_pair[1] in tsym_pair):
                    for isym_pair in src_markets:  # intermediary on source exchange
                        if isym_pair != sym_pair and isym_pair != tsym_pair:
                            if isym_pair[0] in sym_pair and isym_pair[0] not in tsym_pair and isym_pair[1] not in sym_pair and isym_pair[1] in tsym_pair:
                                current_routes.append(self.generate_route(sym_pair, tsym_pair, "source_intermediary", isym_pair,isym_pair[1]))
                            if isym_pair[0] not in sym_pair and isym_pair[0] in tsym_pair and isym_pair[1] in sym_pair and isym_pair[1] not in tsym_pair:
                                current_routes.append(self.generate_route(sym_pair, tsym_pair, "source_intermediary", isym_pair,isym_pair[1]))

        if len(current_routes) != 0:
            exchange_pair = src_exchange + "-" + trgt_exchange
            self.routes[exchange_pair] = current_routes

