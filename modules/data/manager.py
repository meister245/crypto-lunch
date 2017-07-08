from modules.data.webscraper import WebScraper
from modules.data.routes import TradeRoutes
from utilities.helper import Util


class DataManager:
    def __init__(self):
        self.scraper = WebScraper()
        self.routes = TradeRoutes()
        self.util = Util()

    def create_json_data(self):
        """ create JSON database files """
        self.reset_json_data()
        self.cx_pairs = {}

        s = self.util.get_current_time()

        # get exchange names
        self.cx_names = self.util.read_json(self.util.FILE_CONFIG)

        # get exchange trading pairs and store them
        for name in self.cx_names['exchanges']:
            self.cx_pairs[name] = self.scraper.get_exchange_trade_pairs(name, self.cx_pairs)

        self.util.write_json_to_file(self.cx_pairs, self.util.FILE_CXPAIRS)

        # generate arbitrage routes between exchanges
        data = self.routes.get_arbitrage_routes()
        self.util.write_json_to_file(data, self.util.FILE_ROUTES)

        print("#### INFO: JSON databases created successfully)")
        print("#### INFO: Duration - %s minutes" % str((self.util.get_current_time() - s) / 60)[:4])

        return

    def update_json_data(self, *args):
        """ create or update existing JSON database files """

        # update exchange trading pairs file
        if args[0] == 'pairs':
            self.cx_names = self.util.read_json(self.util.FILE_CONFIG)
            self.cx_pairs = self.util.read_json(self.util.FILE_CXPAIRS)

            if self.cx_names == {}:
                self.update_json_data('names')

            for arg in args[1]:
                for idx, name in enumerate(self.cx_names['exchanges']):
                    if arg == name.lower():
                        self.cx_pairs[name] = self.scraper.get_exchange_trade_pairs(name, self.cx_pairs)
                        print("#### INFO: Updated trade pairs for '%s'" % name)
                        break
                    elif idx + 1 == len(self.cx_names['exchanges']):
                        print("#### WARNING: No exchange name value '%s' exists in JSON database" % arg)

            self.util.write_json_to_file(self.cx_pairs, self.util.FILE_CXPAIRS)

        # update exchange arbitrage routes file
        if args[0] == 'routes':
            data = self.routes.get_arbitrage_routes()
            self.util.write_json_to_file(data, self.util.FILE_ROUTES)
            print("#### INFO: Generated arbitrage routes")

        return

    def reset_json_data(self):
        """ reset JSON database files """
        file_paths = [self.util.FILE_CXPAIRS, self.util.FILE_ROUTES]

        for p in file_paths:
            self.util.check_path(p)

        [self.util.write_json_to_file({}, p) for p in file_paths]

        print("#### INFO: JSON databases reset")

        return
