import argparse

from modules.db_manager import DBManager


class App:
    def __init__(self):
        self.args = vars(self.parse_args())
        self.db = DBManager()

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--db_reset', action='store_true', help='reset current database')
        return parser.parse_args()


if __name__ == '__main__':
    app = App()

    if app.args['db_reset']:
        app.db.create_json_data()

