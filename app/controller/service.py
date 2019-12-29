import os
from os.path import join, isdir

from .. import RESOURCES_DIR
from ..controller.data import DataController

import yaml


class ServiceController(object):
    data_ctr = DataController()

    @staticmethod
    def get_config():
        with open(join(RESOURCES_DIR, 'config.yaml')) as f:
            return yaml.load(f.read(), Loader=yaml.BaseLoader)

    @classmethod
    def run_service(cls, source_cx=None, target_cx=None, refresh=False):
        config = cls.get_config()
        exclude, sym_fiat = tuple(config.get('cx_exclude', [])), tuple(config.get('sym_fiat', ()))

        if refresh or not isdir(join(RESOURCES_DIR, 'data') or len(os.listdir(join(RESOURCES_DIR, 'data'))) == 0):
            cls.data_ctr.refresh_data_files()

        if source_cx not in cls.data_ctr.get_cx_names(exclude=exclude):
            raise ValueError(f'invalid source exchange {source_cx}')

        if target_cx not in cls.data_ctr.get_cx_names(exclude=exclude):
            raise ValueError(f'invalid target exchange {target_cx}')

        cx_routes = cls.data_ctr.get_cx_routes(source_cx, target_cx, exclude=exclude, sym_fiat=sym_fiat)
