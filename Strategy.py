import alpaca_trade_api as tradeapi
import json
import pandas as pd
import websocket
import threading
from datetime import datetime, timedelta

from query import *

# Alpaca endpoint
alpaca_paper_endpoint = 'https://paper-api.alpaca.markets'

# Keys to authenticate my account
# Stored as a dictionary
keys = json.loads(open("secret.txt", 'r').read())

# Global variable to store the endpoint of streaming data
# This is for websocket connection
endpoint_wss = "wss://stream.data.alpaca.markets/v2/{}".format("iex")

# Global variable to store alpaca's api to place orders
api = tradeapi.REST(keys["APCA-API-KEY-ID"],
                    keys["APCA-API-SECRET-KEY"], base_url=alpaca_paper_endpoint)


class top_gainer_strategy:
    def __init__(self, ticker_list, max_position_limit):
        self.tickers = ticker_list
        self.historical_data = extract_bars(
            ticker_list, timeframe="1Day", limit=2, start=(
                datetime.now()-timedelta(1)).strftime("%Y-%m-%d"))
        self.last_traded_p = {}
        self.prev_close = {}
        self.percent_change = {}
        self.traded_tickers = []
        self.position_limit = max_position_limit
        self.instantiate()

    def instantiate(self):
        # For all given tickers instantiate the close and last traded price to yesterday's close price
        for ticker in self.tickers:
            self.prev_close[ticker] = self.historical_data[ticker]["close"][-2]
            self.last_traded_p[ticker] = self.historical_data[ticker]["close"][-2]
            self.percent_change[ticker] = 0

    def stream_data(self):
        ws = websocket.WebSocketApp(
            endpoint_wss, on_open=self.on_open, on_message=self.on_message)
        ws.run_forever()

    def on_open(self, ws):
        # Authenticate web socket connections
        auth = {"action": "auth",
                "key": keys["APCA-API-KEY-ID"], "secret": keys["APCA-API-SECRET-KEY"]}
        message = {"action": "subscribe", "trades": self.tickers}
        ws.send(json.dumps(auth))
        ws.send(json.dumps(message))

    def on_message(self, ws, message):
        # Upon recieving the live data for a particular ticker
        # Update the percentage change for the ticker being streamed
        tick_message = json.loads(message)[0]
        sym = tick_message["S"]
        self.last_traded_p[sym] = tick_message["p"]
        self.percent_change[sym] = (
            self.last_traded_p[sym]/self.prev_close[sym] - 1)*100

    def execute_trades(self):
        # For each ticker and it's percentage change
        for ticker, pc in self.percent_change.items():
            # If percentage change greater than 2 then it is not traded yet
            if pc > 2 and ticker not in self.traded_tickers:
                # Then place a buy order for that particular ticker
                api.submit_order(ticker, self.get_quantity(
                    ticker), "buy", "market", "ioc")
                time.sleep(1)
                try:
                    # If the buy order is filled
                    # Place a trailing stop sell order
                    filled_qty = int(api.get_position(ticker).qty)
                    time.sleep(1)
                    api.submit_order(
                        ticker, filled_qty, "sell", "trailing_stop", trail_percent=2)
                    self.traded_tickers.append(ticker)
                except Exception as e:
                    print(ticker, e)

    # Get's maximum quantity that can be used to trade
    def get_quantity(self, ticker):
        return int(self.position_limit/self.last_traded_p[ticker])

    # The strategy runs for the time duration given in the argument
    # Time duration is typically for 1-2 hour when the market opens
    # where trading volume is the highest
    def run_strategy(self, duration):
        # Uses threading to stream live market data
        thread = threading.Thread(target=self.stream_data, daemon=True)
        thread.start()

        start_time = time.time()
        timeout = start_time + duration
        while time.time() <= timeout:
            for ticker in self.tickers:
                print("percentage change for {}  is {}".format(
                    ticker, self.percent_change[ticker]))

                # Execute trades
                self.execute_trades()

            # Put the program to sleep for time taken to run one loop
            time.sleep(60-((time.time() - start_time) % 60))

        # Abort all orders and positions that have not been filled once the time duration is up
        api.cancel_all_orders()
        api.close_all_positions()
