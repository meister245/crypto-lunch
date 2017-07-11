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
        parser.add_argument('--arbitrage_all', action='store_true', help='calculate all arbitrage possibilities')
        parser.add_argument('--arbitrage_source', action='store', help='calculate all arbitrage if source exchanges(s)', default='')
        parser.add_argument('--arbitrage_target', action='store', help='calculate all arbitrage if target exchanges(s)', default='')
        return parser


if __name__ == '__main__':
    app = App()

    if len(sys.argv) == 1:
        app.parser.print_help()
        exit()

    if app.args['arbitrage_all']:
        app.arbitrage.start_service()
        exit()

    if len(app.args['arbitrage_source']) != 0:
        filter = app.args['arbitrage_source'].lower().split(',')
        app.arbitrage.start_service('source', filter)
        exit()

    if len(app.args['arbitrage_target']) != 0:
        filter = app.args['arbitrage_target'].lower().split(',')
        app.arbitrage.start_service('target', filter)
        exit()

    if app.args['names']:
        app.db.get_cx_names()
        exit()

    if app.args['pairs']:
        app.db.create_cx_pairs()
        exit()

    if app.args['routes']:
        app.db.create_cx_routes()
        exit()

    if app.args['reset']:
        app.db.reset_json_data()
        exit()
