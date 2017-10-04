# CryptoLunch

Find profitable arbitrage trading routes for altcoins on crypto exchanges.  
All information is provided by CryptoCompare API.

### Disclaimer

The calculated profit margin does not take into account the withdraw fees, taker fees or any exchange specific fees.  
Always verify the results before taking any actions.

### How to run:

* Python 3.6 required
* Clone repository
* Install any required packages
* Run the commands in the below order.

`python app.py --names`  
Retrieve all exchange names and write them to file.

`python app.py --pairs`  
Retrieve all trading pairs on exchanges and write them to file.

`python app.py --routes`  
Calculate possible arbitrage routes between exchanges and write them to file.

`python app.py --arbitrage_all`  
Run calculation on all possible arbitrage routes and write profitable routes to file.

### Results

View results in `cx_profit.json` located in the `json` folder.

Example:
`"Kraken-Liqui": [{"arbitrage_sym": "DASH", "source_market_pair": "DASH-USD", "source_intermediary": "USDT-USD", "target_market_pair": "DASH-USDT", "helper_sym": "USDT", "source_market_price": 294.9, "source_intermediary_price": 0.9989, "target_market_price": 289.76818641, "profit_margin": "1.883"}]`

1) Source exchange is Kraken, where we have X amount of DASH.
2) Sell DASH for USD, then buy USDT with USD.
3) Transfer USDT to Liqui exchange, sell USDT for DASH.
4) You know have 1.883 times more DASH**

** Exchange fees not included

### Optional

`python app.py --arbitrage_source bittrex`  
`python app.py --arbitrage_source bittrex,poloniex`  
Run calculation on arbitrage routes with designated exchange(s) as source

`python app.py --arbitrage_target bittrex`  
`python app.py --arbitrage_target bittrex,poloniex`  
Run calculation on arbitrage routes with designated exchange(s) as target

### Config

`profit_margin`  
Only write arbitrage routes to file, if the achievable profit % is larger than this decimal value.

`excluded`  
Exclude these exchanges from arbitrage route calculation
