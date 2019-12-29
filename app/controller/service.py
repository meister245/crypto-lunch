import os
from os.path import join, isdir

from .. import RESOURCES_DIR
from ..controller.data import DataController
from ..controller.arbitrage import ArbitrageController

import yaml


class ServiceController(object):
    data_ctr = DataController()
    arbitrage_ctr = ArbitrageController()

    @classmethod
    def run_service(cls, source_cx, target_cx, refresh=False, **kwargs):
        config = cls.get_config()
        exclude, sym_fiat = tuple(config.get('cx_exclude', [])), tuple(config.get('sym_fiat', ()))

        if refresh or not isdir(join(RESOURCES_DIR, 'data') or len(os.listdir(join(RESOURCES_DIR, 'data'))) == 0):
            cls.data_ctr.refresh_data_files()

        source_cx = cls.get_cx_name(source_cx, exclude=exclude)
        target_cx = cls.get_cx_name(target_cx, exclude=exclude)

        cx_routes = cls.data_ctr.get_cx_routes(source_cx, target_cx, exclude=exclude, sym_fiat=sym_fiat)
        profit_routes = cls.arbitrage_ctr.run_arbitrage(cx_routes, profit_margin=kwargs.get('profit_margin', 1.0))

        for cx_pair, routes in profit_routes.items():
            for route in routes:
                cls.display_route(cx_pair, route)

    @staticmethod
    def get_config():
        with open(join(RESOURCES_DIR, 'config.yaml')) as f:
            return yaml.load(f.read(), Loader=yaml.BaseLoader)

    @classmethod
    def get_cx_name(cls, name, exclude):
        for s_cx in cls.data_ctr.get_cx_names(exclude=exclude):
            if name == s_cx.lower():
                return s_cx

        raise ValueError(f'invalid exchange name - {name}')

    @staticmethod
    def display_route(cx_pair, route):
        cx_s, cx_t = cx_pair.split('-')
        cx_i = f'{cx_s if "source_intermediary" in route else cx_t}'
        pair_i = f'{route["source_intermediary"] if "source_intermediary" in route else route["target_intermediary"]}'

        print(f'arbitrage: {route["arbitrage_sym"]} - profit margin: {round(route["profit_margin"], 2)})')
        print(f'{route["source_market_pair"]} ({cx_s}) => {pair_i} ({cx_i}) => {route["target_market_pair"]} ({cx_t})')
