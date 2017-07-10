import os
import json
import time


class Util:
    def __init__(self):
        self.CONFIG = 'config.json'
        self.FILE_NAMES = 'json/cx_names.json'
        self.FILE_PAIRS = 'json/cx_pairs.json'
        self.FILE_ROUTES = 'json/cx_routes.json'
        self.FILE_PROFIT = 'json/cx_profit.json'

    @staticmethod
    def read_file(filename):
        with open(filename, 'r') as f:
            return [i for i in f]

    @staticmethod
    def write_json_to_file(data, filename):

        dirname, file = filename.split('/')

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as f:
            return json.dump(data, f)

    @staticmethod
    def read_json(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return dict()
