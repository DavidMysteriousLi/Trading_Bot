# Module for extracting historical market data

import requests
import json
import pandas as pd
import time
from datetime import datetime, timedelta

# Keys to authenticate my account
# Stored as a dictionary
keys = json.loads(open("secret.txt", 'r').read())

# Global variable to store the endpoint of historical market data
# This is for http connection
endpoint_md = "https://data.alpaca.markets/v2/"

# Extract information about the given stock(s) 
# Return a dictionary with ticker as it's key and dataframe of bar information as it's item

def extract_bars(symbols, timeframe, limit, start, end=""):
    dict_df = {}
    for ticker in symbols:
        bar_url = endpoint_md + "stocks/{}/bars".format(ticker)
        parameters = {"limit": limit, "timeframe": timeframe,
                      "start": start, "end": end}

        r = requests.get(bar_url, headers=keys, params=parameters)
        df_data = r.json()
        temp = pd.DataFrame(df_data["bars"])
        temp.rename({"t": "time", "o": "open", "h": "high",
                    "l": "low", "c": "close", "v": "volume"}, axis=1, inplace=True)
        temp["time"] = pd.to_datetime(temp["time"])
        temp.set_index("time", inplace=True)
        dict_df[ticker] = temp
    return dict_df

# Example of using extract bars: 
# msg = extract_bars(["AAPL, BB"], timeframe="1Day", limit=100, start="2022-01-01")
# print(msg)
