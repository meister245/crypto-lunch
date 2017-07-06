from utilities.helper import Util


class ArbitrageRoutes:
    def __init__(self):
        self.util = Util()

    def get_arbitrage_routes(self):
        data = self.util.read_json(self.util.FILE_CXPAIRS)

