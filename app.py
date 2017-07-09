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
        parser.add_argument('--db_create', action='store_true', help='generate new json database')
        parser.add_argument('--db_update_pairs', action='store', type=str, help='update exchange pairs')
        parser.add_argument('--db_update_routes', action='store_true', help='update arbitrage routes')
        parser.add_argument('--db_reset', action='store_true', help='reset to empty json database')

        parser.add_argument('--arbitrage', action='store_true', help='calculate arbitrage possibilities')

        return parser


if __name__ == '__main__':
    app = App()

    if len(sys.argv) == 1:
        app.parser.print_help()
        exit()

    if app.args['arbitrage']:
        app.arbitrage.start_service()
    elif app.args['db_create']:
        app.db.create_json_data()
    elif app.args['db_reset']:
        app.db.reset_json_data()
    else:
        if app.args['db_update_pairs'] is not None:
            app.db.update_json_data('pairs', app.args['db_update_pairs'].split(','))
        if app.args['db_update_routes']:
            app.db.update_json_data('routes')
