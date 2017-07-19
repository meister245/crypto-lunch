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

### Options

`python app.py --names`  
Retrieve all exchange names and write them to file.

`python app.py --pairs`  
Retrieve all trading pairs on exchanges and write them to file.

`python app.py --routes`  
List all possible arbitrage routes between exchanges and write them to file.

`python app.py --arbitrage_all`  
Run calculation on all possible arbitrage routes and write profitable routes to file.

`python app.py --arbitrage_source bittrex`  
`python app.py --arbitrage_source bittrex,poloniex`  
Run calculation on arbitrage routes with designated exchange(s) as source

`python app.py --arbitrage_target bittrex`  
`python app.py --arbitrage_target bittrex,poloniex`  
Run calculation on arbitrage routes with designated exchange(s) as target

### Config

`profit_margin`  
Only write arbitrage routes to file, if the achievable profit % is larger than this value.

`excluded`  
Exclude these exchanges from arbitrage route calculation