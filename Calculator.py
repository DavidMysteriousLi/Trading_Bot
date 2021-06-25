import pandas_datareader as pdr
import pandas as pd
import datetime as dt
from datetime import timedelta

def calc_MA_RSI(symbol):

    #Collecting data of the ticker from yahoo finance
    time_now = dt.datetime.now()
    time_1_year_ago = time_now - timedelta(days=365)
    data = pdr.get_data_yahoo(symbol, time_1_year_ago)
    data.index = data.index.date

    #Calculating moving average
    moving_close = pd.DataFrame(data.Close)
    moving_close_1 = data['Close']
    MA_result = moving_close_1.rolling(window=200).mean()
    MA_value =  MA_result[-1].item()

    #Calculating RSI value
    delta = data['Close'].diff(1)
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    down = -1 * down

    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up / ema_down
    data['RSI'] = 100 - (100/ (1 + rs))
    RSI_value = data['RSI'][-1].item()

    return (MA_value, RSI_value)
