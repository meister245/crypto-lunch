import json


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
