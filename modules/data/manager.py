from modules.data.webscraper import WebScraper
from utilities.helper import Util


class DataManager:
    def __init__(self):
        self.scraper = WebScraper()
        self.util = Util()

    def create_json_data(self):
        self.reset_json_data()
        self.cx_pairs = {}

        s = self.util.get_current_time()

        # get exchange names and store them
        self.cx_names = self.scraper.get_exchange_names()
        self.util.write_json_to_file(self.cx_names, self.util.FILE_CXNAMES)

        # get exchange trading pairs and store them
        for name in self.cx_names['exchanges']:
            self.cx_pairs[name] = self.scraper.get_exchange_trade_pairs(name, self.cx_pairs)

        self.util.write_json_to_file(self.cx_pairs, self.util.FILE_CXPAIRS)

        print("#### INFO: Database created successfully)")
        print("#### INFO: Duration - %s minutes" % str((self.util.get_current_time() - s) / 60)[:4])

        return

    def update_json_data(self, *args):
        """ update existing JSON json / create JSON json with selected exchanges """

        if args[0] == 'names':
            self.cx_names = self.scraper.get_exchange_names()
            self.util.write_json_to_file(self.cx_names, self.util.FILE_CXNAMES)
            print("#### INFO: Updated exchange names")

        if args[0] == 'pairs':
            self.cx_names = self.util.read_json(self.util.FILE_CXNAMES)
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
                        print("#### WARNING: No exchange name value '%s' exists in json database" % arg)

            self.util.write_json_to_file(self.cx_pairs, self.util.FILE_CXPAIRS)

        return

    def reset_json_data(self):
        file_paths = [self.util.FILE_CXNAMES, self.util.FILE_CXPAIRS]

        for p in file_paths:
            self.util.check_path(p)

        return [self.util.write_json_to_file({}, p) for p in file_paths]
