from modules.data.routes import TradeRoutes
from modules.data.pairs import TradePairs
from utilities.helper import Util


class DataManager:
    def __init__(self):
        self.util = Util()

    def get_cx_names(self):
        """ generate exchange names """
        self.pairs = TradePairs()

        self.cx_names = {"exchanges": self.pairs.get_exchange_names()}
        self.util.write_json_to_file(self.cx_names, self.util.FILE_NAMES)

        print("#### INFO: Generated exchange names")
        return

    def create_cx_pairs(self):
        """ generate exchange trading pairs """
        self.pairs = TradePairs()

        self.cx_pairs = self.pairs.get_trade_pairs()
        self.util.write_json_to_file(self.cx_pairs, self.util.FILE_PAIRS)

        print("#### INFO: Generated exchange trading pairs")
        return

    def create_cx_routes(self):
        """ generate arbitrage routes between exchanges """
        self.routes = TradeRoutes()

        data = self.routes.get_arbitrage_routes()
        self.util.write_json_to_file(data, self.util.FILE_ROUTES)

        print("#### INFO: Generated arbitrage routes")
        return

    def reset_json_data(self):
        """ reset JSON data files """
        file_paths = [self.util.FILE_PAIRS, self.util.FILE_ROUTES, self.util.FILE_NAMES, self.util.FILE_PROFIT]

        [self.util.write_json_to_file({}, p) for p in file_paths]

        print("#### INFO: JSON data files reset")
        return
