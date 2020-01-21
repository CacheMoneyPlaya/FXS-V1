from datetime import datetime
from yahoo_fin import stock_info as si
from datetime import date
import pandas as pd
import time
import pytz
import numpy as np
import yfinance as yf
import csv

historicalData = {}

def setPriorTickerData(tickers):
    # Get Historical data 1 day prior in 1 min increments
    for t in tickers:
        historicalData.update({t: pd.DataFrame(yf.download(tickers = t,period = '1d',interval = '1m').Open)})
        path = "C:/Users/User/Documents/Tests/FXS-V1/TickerData"+"/"+str(t)+".xlsx"
        historicalData[t].to_csv(path, index=True)
    run(tickers)

def run(tickers):
    now_UTC = datetime.now(pytz.timezone('US/Eastern'))
    while now_UTC.hour < 14:
        for t in tickers:
            path = "C:/Users/User/Documents/Tests/FXS-V1/TickerData"+"/"+str(t)+".xlsx"
            # Get stock data
            # Every minute create a new row on top of existing data with new ask
            live_ask = si.get_live_price(t)
            print(t + ' --> ' + str(live_ask))
            concurrent_time = datetime.now().strftime("%Y-%m-%d %H:%M:00-05:00")
            # Write the concurrent minute value to existing csv
            with open(path,'a', newline='') as f:
                writer=csv.writer(f)
                writer.writerow([str(concurrent_time), str(live_ask)])
            # Calculate moving averages across Fibonacci time frames   
        print('Analysis Complete')    
        time.sleep(5)
    exit()

    # Calculate the moving average , 5minMA and 15 minMA (check fibonacci seq) concurrent value
    # If buy signal, buy, store this as an actively open position and remove stock from tickers while in position
    # Run the activity check on stock to look for sell signal