# Trading Bot! 

 ## 1) Top gainer strategy: 

* Market condition:
    - Start running the algorithm when the market opens (When trading volume is typically the highest)
    - The algorithm typically runs for 1 - 2 hours.

* The steps of the strategy are as follows :
    - When a stock's gain percentage exceeds +1% place a buy order on the stock
    - After that, place a trailing stop loss on the stock at trail percent = 3
    - Exit all orders on a 3% gain or EOD
