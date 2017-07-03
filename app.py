import argparse

from modules.data_manager import DataManager


class App:
    def __init__(self):
        self.args = vars(self.parse_args())
        self.db = DataManager()

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--db_create', action='store_true', help='generate new json database')
        parser.add_argument('--db_update_names', action='store_true', help='update exchange names')
        parser.add_argument('--db_update_pairs', action='store', type=str, help='update exchange pairs')
        parser.add_argument('--db_reset', action='store_true', help='reset to empty json database')
        return parser.parse_args()


if __name__ == '__main__':
    app = App()

    if app.args['db_create']:
        app.db.create_json_data()
    elif app.args['db_reset']:
        app.db.reset_json_data()
    else:
        if app.args['db_update_names']:
            app.db.update_json_data('names')
        if app.args['db_update_pairs'] is not None:
            app.db.update_json_data('pairs', app.args['db_update_pairs'].split(','))
