from utilities.helper import Util
from modules.api.cryptocompare_api import CryptoCompareAPI


class TradePairs:
    def __init__(self):
        self.api = CryptoCompareAPI()
        self.util = Util()

    def get_exchange_names(self):
        return [k for k in self.api.get_exchange_pairs().keys()]

    def get_trade_pairs(self):
        response = self.api.get_exchange_pairs()
        excluded_exchanges = self.util.read_json(self.util.CONFIG)['excluded']
        pairs = {}

        for cx_name, cx_pairs in response.items():
            if cx_name not in excluded_exchanges:
                pairs[cx_name] = {}
                for key_fsym, list_tsyms in cx_pairs.items():
                    for sym in list_tsyms:
                        if sym not in pairs[cx_name].keys():
                            pairs[cx_name][sym] = []

                        pairs[cx_name][sym].append(key_fsym)

                    if len(pairs[cx_name][sym]) == 0:
                        del pairs[cx_name][sym]

                if len(cx_pairs) == 0:
                    del pairs[cx_name]

        return pairs