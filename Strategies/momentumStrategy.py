from datetime import datetime
from yahoo_fin import stock_info as si
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import yfinance as yf

data = {}

def setPriorTickerData(ticker):
    # Get Historical data 1-2 days prior in 1 min increments
    data.update({ticker: pd.DataFrame(yf.download(tickers = ticker,period = '1d',interval = '1m').Open)})

def run(ticker):
    # Every minute create a new row ontop of exisitng data with new ask
    live_ask = si.get_live_price(ticker)
    concurrent_time = datetime.now().strftime("%Y-%m-%d %H:%M:00 - 05:00")
    data[ticker].loc[concurrent_time, 'Open'] = live_ask

    # Calculate the moving average , 5minMA and 15 minMA (check fibonacci seq) concurrent value
    # If buy signal, buy, store this as an actively open position and remove stock from tickers while in position
    # Run the activity check on stock to look for sell