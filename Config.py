import alpaca_trade_api as tradeapi
from Calculator import *

class Long_pull_strategy:
    def __init__(self, ticker_list):
        self.key = 'PKPH47Q222AVQZ6C9F8B'
        self.secret = 'WGYvRUIYa2Bu4cyuBEl1Gh9A3apFj2CEeVgRBjZh'
        self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
        self.api = tradeapi.REST(self.key, self.secret, self.alpaca_endpoint)
        self.symbols = ticker_list
        self.satisfied_tickers = []
        self.MA_RSI = ()
        self.portfolio = self.api.list_positions()
        
    def generate_satisfied_tickers(self):
        for ticker in self.symbols:
            latest_trade_price = self.api.get_latest_trade(ticker).p
            self.MA_RSI += calc_MA_RSI(ticker)
            ma_value = self.MA_RSI[0]
            rsi_value = self.MA_RSI[1]
            if (latest_trade_price > ma_value and rsi_value < 35):
                self.satisfied_tickers.append(ticker)
            self.MA_RSI = ()
        return

    def get_satisfied_ticker(self):
        return self.satisfied_tickers

    def create_buy_order(self):
        if self.satisfied_tickers == []:
            print("No stock that satisfies the long pull back strategy")
            return        
        account = self.api.get_account()
        if float(account.cash) <= 0:
            print("No cash available to buy")
            return

        buy_ticker_cash = float(account.cash) / len(self.satisfied_tickers)
        for ticker in self.satisfied_tickers:
            ticker_price = self.api.get_latest_trade(ticker).p
            quantity = round(buy_ticker_cash / ticker_price)
            print(f'Filling Buy order of ' + ticker + f' at $ {ticker_price} for {quantity} shares')
            self.api.submit_order(
                symbol= ticker, 
                qty= quantity, 
                side= "sell", 
                type= "market",
                time_in_force= "day")
            print(f'buy order of {ticker} is filled')
        return
    
    def create_sell_order(self):
        for position in self.portfolio:
            self.MA_RSI += calc_MA_RSI(position.symbol)
            rsi_value = self.MA_RSI[1]
            if (rsi_value > 45):
                print(f'Filling sell order of ' + position.symbol + ' at '\
                    '$ ' + position.current_price + ' for ' +  position.qty + ' shares')
                self.api.submit_order(
                    symbol= position.symbol, 
                    qty= position.qty, 
                    side= "buy", 
                    type= "market",
                    time_in_force= "day")
                print(f'sell order of ' + position.symbol + ' is filled')
            self.MA_RSI = ()
        return

