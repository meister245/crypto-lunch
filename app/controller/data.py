import os
import json
import shutil
from os.path import join, isdir, isfile

from .. import RESOURCES_DIR

import cachetools.func

from lib.cryptocompare import CryptoCompareAPI


class DataController(object):
    api = CryptoCompareAPI()

    @classmethod
    @cachetools.func.lfu_cache()
    def get_cx_names(cls, exclude):
        if isdir(join(RESOURCES_DIR, 'data')) and isfile(join(RESOURCES_DIR, 'data', 'cx_names.dat')):
            with open(join(RESOURCES_DIR, 'data', 'cx_names.dat')) as f:
                return tuple([x for x in f.read().split(',')])

        cx_names = tuple([x for x in cls.api.get_exchange_pairs() if x not in exclude])

        if len(cx_names) > 0:
            cls.write_data_file(cx_names, f_name='cx_names.dat', df='csv')

        return cx_names

    @classmethod
    @cachetools.func.lfu_cache()
    def get_cx_pairs(cls, exclude):
        if isdir(join(RESOURCES_DIR, 'data')) and isfile(join(RESOURCES_DIR, 'data', 'cx_pairs.dat')):
            with open(join(RESOURCES_DIR, 'data', 'cx_pairs.dat')) as f:
                return json.loads(f.read())

        cx_pairs = {}

        for cx_name, sym_pairs in cls.api.get_exchange_pairs().items():
            pairs = {}

            if cx_name in exclude:
                continue

            for sym_src, sym_target in sym_pairs.items():
                pairs.update({sym_src: tuple(sym_target)})

            if len(sym_pairs) > 0:
                cx_pairs.update({cx_name: sym_pairs})

        if len(cx_pairs) > 0:
            cls.write_data_file(cx_pairs, f_name='cx_pairs.dat', df='json')

        return cx_pairs

    @classmethod
    @cachetools.func.lfu_cache()
    def get_cx_routes(cls, src_cx, target_cx, exclude=None, sym_fiat=None):
        f_name = f'{src_cx}-{target_cx}.dat'

        if isdir(join(RESOURCES_DIR, 'data', 'cx_routes')) and isfile(join(RESOURCES_DIR, 'data', 'cx_routes', f_name)):
            with open(join(RESOURCES_DIR, 'data', 'cx_routes', f_name)) as f:
                return json.loads(f.read())

        cx_pairs = cls.get_cx_pairs(exclude=exclude)
        cx_routes = {f'{src_cx}-{target_cx}': cls.find_routes(cx_pairs, sym_fiat, src_cx, target_cx)}

        if len(cx_routes) > 0:
            cls.write_data_route_file(cx_routes, f_name)

        return cx_routes

    @classmethod
    def find_routes(cls, cx_pairs, sym_fiat, src_cx, target_cx):
        current_routes = []

        for src_pair in cls.list_trading_pairs(cx_pairs, src_cx):
            for target_pair in cls.list_trading_pairs(cx_pairs, target_cx):
                src_base, src_quote = src_pair
                target_base, target_quote = target_pair

                # intermediary trading pair on target exchange:
                if src_base in target_pair and src_quote not in target_pair:
                    if src_base not in sym_fiat and src_quote not in sym_fiat:
                        for inter_pair in cls.list_trading_pairs(cx_pairs, target_cx):
                            if inter_pair != src_pair and inter_pair != target_pair:
                                for x in cls.find_intermediary_markets(src_pair, target_pair, inter_pair, 'target'):
                                    print(f'{len(current_routes) + 1} routes - {src_cx} -> {target_cx}\r', end='')
                                    current_routes.append(x)

                # intermediary trading pairs on source exchange:
                if src_base in target_pair and src_quote not in target_pair:
                    if src_base not in sym_fiat and target_base not in sym_fiat and target_quote not in sym_fiat:
                        for inter_pair in cls.list_trading_pairs(cx_pairs, src_cx):
                            if inter_pair != src_pair and inter_pair != target_pair:
                                for x in cls.find_intermediary_markets(src_pair, target_pair, inter_pair, 'source'):
                                    print(f'{len(current_routes) + 1} routes - {src_cx} -> {target_cx}\r', end='')
                                    current_routes.append(x)

        if len(current_routes) > 0:
            print(f'{len(current_routes)} routes - {src_cx} -> {target_cx}')

        return current_routes

    @staticmethod
    def list_trading_pairs(cx_pairs, exchange_name):
        for base_sym, target_syms in cx_pairs[exchange_name].items():
            for sym in target_syms:
                yield tuple([sym, base_sym])

    @classmethod
    def generate_route(cls, src_pair, target_pair, inter_type, inter_pair):
        return {
            f'arbitrage_sym': src_pair[0],
            f'source_market_pair': '-'.join(src_pair),
            f'target_market_pair': '-'.join(target_pair),
            f'{inter_type}_intermediary': '-'.join(inter_pair),
            f'helper_sym': cls.get_helper_sym(src_pair, target_pair)
        }

    @classmethod
    def find_intermediary_markets(cls, src_pair, target_pair, inter_pair, inter_type):
        inter_base, inter_quote = inter_pair

        if inter_base in src_pair and inter_base not in target_pair and inter_quote not in src_pair and inter_quote in target_pair:
            yield cls.generate_route(src_pair, target_pair, inter_type, inter_pair)

        if inter_base not in src_pair and inter_base in target_pair and inter_quote in src_pair and inter_quote not in target_pair:
            yield cls.generate_route(src_pair, target_pair, inter_type, inter_pair)

    @staticmethod
    def get_helper_sym(source_pair, target_pair):
        for sym in target_pair:
            if sym not in source_pair:
                return sym

    @classmethod
    def refresh_data_files(cls):
        if isdir(join(RESOURCES_DIR, 'data')):
            shutil.rmtree(join(RESOURCES_DIR, 'data'))

        cls.get_cx_names.cache_clear()
        cls.get_cx_pairs.cache_clear()
        cls.get_cx_routes.cache_clear()

    @classmethod
    def write_data_file(cls, data, f_name, df='json'):
        if not isdir(join(RESOURCES_DIR, 'data')):
            os.mkdir(join(RESOURCES_DIR, 'data'))

        with open(join(RESOURCES_DIR, 'data', f_name), 'w') as f:
            f.write(json.dumps(data) if df == 'json' else ','.join(data) if df == 'csv' else data)

    @classmethod
    def write_data_route_file(cls, data, f_name):
        if not isdir(join(RESOURCES_DIR, 'data', 'cx_routes')):
            os.mkdir(join(RESOURCES_DIR, 'data', 'cx_routes'))

        with open(join(RESOURCES_DIR, 'data', 'cx_routes', f_name), 'w') as f:
            f.write(json.dumps(data))
