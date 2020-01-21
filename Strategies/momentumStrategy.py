from datetime import datetime
from yahoo_fin import stock_info as si
from datetime import date
from dotenv import load_dotenv
import os
import pandas as pd
import time
import pytz
import numpy as np
import yfinance as yf
import csv
import matplotlib.pyplot as plt 

historicalData = {}
load_dotenv('.env')

def setPriorTickerData(tickers):
    # Get Historical data 1 day prior in 1 min increments
    for t in tickers:
        historicalData.update({t: pd.DataFrame(yf.download(tickers = t,period = '1d',interval = '1m').Open)})
        path = str(os.getenv('TICKER_DATA_PATH'))+"/"+str(t)+".xlsx"
        historicalData[t].to_csv(path, index=True)
    run(tickers)

def run(tickers):
    now_UTC = datetime.now(pytz.timezone('America/New_York'))
    while now_UTC.hour < 16:
        for t in tickers:
            path = str(os.getenv('TICKER_DATA_PATH'))+"/"+str(t)+".xlsx"
            # Get stock data, every minute create a new row on top of existing data with new ask
            live_ask = si.get_live_price(t)
            print('\033[92m' + t + ' --> ' + str(live_ask))
            concurrent_time = datetime.now(pytz.timezone('America/New_York')).strftime("%Y-%m-%d %H:%M:00-05:00")
            # Write the concurrent minute value to existing csv
            with open(path,'a', newline='') as f:
                writer=csv.writer(f)
                writer.writerow([str(concurrent_time), str(live_ask)])
            # Calculate moving averages across Fibonacci time frames   
            momentumSignal(t)
        print('\033[91m' + 'Analysis Complete')    
        time.sleep(60)
    print('Markets are currently closed...')
    exit()

    # Calculate the moving average , 5minMA and 15 minMA (check fibonacci seq) concurrent value
    # If buy signal, buy, store this as an actively open position and remove stock from tickers while in position
    # Run the activity check on stock to look for sell signal

def momentumSignal(t):
    df = pd.read_csv(str(os.getenv('TICKER_DATA_PATH'))+"/"+"BNTX"+".xlsx", index_col="Datetime")
    short_rolling = df.rolling(window=8).mean()
    long_rolling = df.rolling(window=30).mean()
    fig = plt.figure()

    for frame in [df.reset_index(),short_rolling.reset_index(), long_rolling.reset_index()]:
        plt.plot(frame['Datetime'], frame['Open'])

    # Currently createds a moving average than a strategy can be modeled around.

    plt.show()


