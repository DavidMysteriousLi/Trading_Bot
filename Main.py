from Strategy import *
from pytickersymbols import PyTickerSymbols


def main():
    # nasdaq_100_tickers = []
    # stock_data = PyTickerSymbols()
    # nasdaq_stocks = list(stock_data.get_stocks_by_index('NASDAQ 100'))
    # for stocks in nasdaq_stocks:
    #     nasdaq_100_tickers.append(stocks["symbol"])

    # nasdaq_100_tickers.remove("CTRP")
    # first_10 = nasdaq_100_tickers[0:9]
    symbols = ["AMC", "FB", "MSFT", "NVDA"]
    strategy = top_gainer_strategy(symbols, 300)
    strategy.run_strategy(60*2)


if __name__ == '__main__':
    main()
