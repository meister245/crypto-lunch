import os
import json
import time


class Util:
    def __init__(self):
        pass

    @staticmethod
    def read_file(filename):
        with open(filename, 'r') as f:
            return [i for i in f]

    @staticmethod
    def write_json_to_file(data, filename):
        with open(filename, 'w') as f:
            return json.dump(data, f)

    @staticmethod
    def read_json(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return dict()

    @staticmethod
    def check_path(p):
        dirname, filename = p.split('/')

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if not os.path.exists(p):
            with open(p, 'w') as f:
                return json.dump({}, f)

    @staticmethod
    def get_current_time():
        return time.time()
