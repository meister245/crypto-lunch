from utilities.helper import Util
from modules.web_scraper import WebScraper


class DataManager:
    def __init__(self):
        self.scraper = WebScraper()

    def create_json_data(self):
        """ get exchange names and associated trade pairs and write them to JSON """
        self.cx_names = self.scraper.get_exchange_names()
        self.cx_pairs = {}

        for name in self.cx_names:
            self.cx_pairs[name] = self.scraper.get_exchange_trade_pairs(name, self.cx_pairs)

        self.write_json(self.cx_names, 'data/cx_names.json')
        self.write_json(self.cx_pairs, 'data/cx_pairs.json')

        return

    def write_json(self, data, path):
        return Util.write_json_to_file(data, path)
