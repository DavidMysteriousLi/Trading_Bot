from Config import *
from pytickersymbols import PyTickerSymbols

def main():
    nasdaq_100_tickers = []
    stock_data = PyTickerSymbols()
    nasdaq_stocks = list(stock_data.get_stocks_by_index('NASDAQ 100'))
    for stocks in nasdaq_stocks:
        nasdaq_100_tickers.append(stocks["symbol"])
    
    nasdaq_100_tickers.remove("CTRP")
    first_10 = nasdaq_100_tickers[0:9]
    long_strategy = Long_pull_strategy(first_10)
    long_strategy.create_sell_order()
    # long_strategy.generate_satisfied_tickers()
    # print(long_strategy.get_satisfied_ticker())
    # long_strategy.create_buy_order()

if __name__ == '__main__':
    main()