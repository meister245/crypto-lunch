import sys
import argparse

from modules.data.manager import DataManager
from modules.service.arbitrage import Arbitrage


class App:
    def __init__(self):
        self.db = DataManager()
        self.arbitrage = Arbitrage()

        self.parser = self.parse_args()
        self.args = vars(self.parser.parse_args())

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--names', action='store_true', help='generate exchange names')
        parser.add_argument('--pairs', action='store_true', help='generate trade pairs')
        parser.add_argument('--routes', action='store_true', help='generate possible arbitrage routes')
        parser.add_argument('--reset', action='store_true', help='delete all json data files')
        parser.add_argument('--arbitrage', action='store_true', help='calculate arbitrage possibilities')
        return parser


if __name__ == '__main__':
    app = App()

    if len(sys.argv) == 1:
        app.parser.print_help()
        exit()

    if app.args['arbitrage']:
        app.arbitrage.start_service()
    elif app.args['names']:
        app.db.get_cx_names()
    elif app.args['pairs']:
        app.db.create_cx_pairs()
    elif app.args['routes']:
        app.db.create_cx_routes()
    elif app.args['reset']:
        app.db.reset_json_data()
