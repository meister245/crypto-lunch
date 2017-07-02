from utilities.helper import Util
from modules.web_scraper import WebScraper

FILE_CXNAMES = 'data/cx_names.json'
FILE_CXPAIRS = 'data/cx_pairs.json'


class DataManager:
    def __init__(self):
        self.scraper = WebScraper()

    def create_json_data(self):
        """ get exchange names and associated trade pairs and write them to JSON """
        self.cx_names = self.scraper.get_exchange_names()
        self.cx_pairs = {}

        for name in self.cx_names:
            self.cx_pairs[name] = self.scraper.get_exchange_trade_pairs(name, self.cx_pairs)

        self.write_json(self.cx_names, FILE_CXNAMES)
        self.write_json(self.cx_pairs, FILE_CXPAIRS)

        return

    def update_json_data(self, *args):
        """ update existing JSON files """

        if args[0] == 'names':
            self.cx_names = self.scraper.get_exchange_names()
            self.write_json(self.cx_names, FILE_CXNAMES)

        if args[0] == 'pairs':
            self.cx_names = self.read_json(FILE_CXNAMES)
            self.cx_pairs = self.read_json(FILE_CXPAIRS)

            for name in self.cx_names:
                if name.lower() in args[1]:
                    self.cx_pairs[name] = self.scraper.get_exchange_trade_pairs(name, self.cx_pairs)

            self.write_json(self.cx_pairs, FILE_CXPAIRS)

        return

    def write_json(self, data, path):
        return Util.write_json_to_file(data, path)

    def read_json(self, path):
        return Util.read_json(path)
