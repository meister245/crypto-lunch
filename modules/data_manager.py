from utilities.helper import Util
from modules.web_scraper import WebScraper

FILE_CXNAMES = 'data/cx_names.json'
FILE_CXPAIRS = 'data/cx_pairs.json'


class DataManager:
    def __init__(self):
        self.scraper = WebScraper()

    def create_json_data(self):
        self.reset_json_data()
        self.cx_pairs = {}

        s = Util.get_current_time()

        # get exchange names and store them
        self.cx_names = self.scraper.get_exchange_names()
        self.write_json_data(self.cx_names, FILE_CXNAMES)

        # get exchange trading pairs and store them
        for name in self.cx_names['exchanges']:
            self.cx_pairs[name] = self.scraper.get_exchange_trade_pairs(name, self.cx_pairs)

        self.write_json_data(self.cx_pairs, FILE_CXPAIRS)

        print("#### INFO: Database created successfully)")
        print("#### INFO: Duration - %s minutes" % str((Util.get_current_time() - s) / 60)[:4])

        return

    def update_json_data(self, *args):
        """ update existing JSON data / create JSON data with selected exchanges """

        if args[0] == 'names':
            self.cx_names = self.scraper.get_exchange_names()
            self.write_json_data(self.cx_names, FILE_CXNAMES)
            print("#### INFO: Updated exchange names")

        if args[0] == 'pairs':
            self.cx_names = self.read_json_data(FILE_CXNAMES)
            self.cx_pairs = self.read_json_data(FILE_CXPAIRS)

            if self.cx_names == {}:
                self.update_json_data('names')

            for arg in args[1]:
                for idx, name in enumerate(self.cx_names['exchanges']):
                    if arg == name.lower():
                        self.cx_pairs[name] = self.scraper.get_exchange_trade_pairs(name, self.cx_pairs)
                        print("#### INFO: Updated trade pairs for '%s'" % name)
                        break
                    elif idx + 1 == len(self.cx_names['exchanges']):
                        print("#### WARNING: No exchange name value '%s' exists in json database" % arg)

            self.write_json_data(self.cx_pairs, FILE_CXPAIRS)

        return

    def write_json_data(self, data, path):
        return Util.write_json_to_file(data, path)

    def read_json_data(self, path):
        return Util.read_json(path)

    def reset_json_data(self):
        file_paths = [FILE_CXNAMES, FILE_CXPAIRS]

        for p in file_paths:
            Util.check_path(p)

        return [self.write_json_data({}, p) for p in file_paths]
