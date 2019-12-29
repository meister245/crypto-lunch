crypto-lunch
------------

Calculate and find high risk arbitrage trading routes for altcoins on cryptocurrency exchanges. Data is fully sourced from CryptoCompare

#### Disclaimer

* The calculated profit margin does not take into account the exchange market order book, exchange withdraw fees, taker fees or any other fees associated with the given exchange
* Any windows of opportunity are likely to be gone under a few minutes
* Always verify open markets and exchange policies before taking any action at your own risk.

#### Setup & Usage:

* Python 3.7.x required
* Clone or download repository
* Install dependency libraries


    pip install -r ./requirements.txt

#### Demo

    ./bin/arbitrage coinbase bittrex

    Coinbase-BitTrex - 152 routes found
    Coinbase-BitTrex - 42 active routes after validation
    Coinbase-BitTrex - 4 profitable routes calculated
    --------------------------------------------------
    Arbitrage Crypto: BTC - Profit Margin: 3.5 %
    BTC-ETH (Coinbase) => ETH-STRAT (BitTrex) => BTC-STRAT (BitTrex)
    --------------------------------------------------
    Arbitrage Crypto: BTC - Profit Margin: 1.37 %
    BTC-ETH (Coinbase) => ETH-DMT (BitTrex) => BTC-DMT (BitTrex)
    --------------------------------------------------
    Arbitrage Crypto: BTC - Profit Margin: 1.03 %
    BTC-ETC (Coinbase) => ETH-ETC (BitTrex) => BTC-ETH (BitTrex)
    --------------------------------------------------
    Arbitrage Crypto: BTC - Profit Margin: 1.33 %
    BTC-EOS (Coinbase) => ETH-EOS (BitTrex) => BTC-ETH (BitTrex)

**Steps**
1. Source exchange is Coinbase, where we have X amount of BTC.
2. Sell BTC for ETH on Coinbase
3. Transfer ETH from Coinbase to BitTrex
4. Sell ETH for STRAT on BitTrex
5. Sell STRAT for BTC on BitTrex
6. You now have 3.5 % more BTC**
7. Transfer BTC back to Coinbase and repeat if still profitable

** See disclaimer above

**Config**

There is a configuration file in `./resources/config.yaml`

`sym_exclude`

Exclude market pairs with these symbols from arbitrage route calculation

`cx_exclude`

Exclude these exchanges from arbitrage route calculation
