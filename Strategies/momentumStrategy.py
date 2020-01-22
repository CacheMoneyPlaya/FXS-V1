from datetime import datetime
from yahoo_fin import stock_info as si
from datetime import date
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
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
api = tradeapi.REST(
    os.getenv('APCA_API_KEY_ID'),
    os.getenv('APCA-API-SECRET-KEY'),
    os.getenv('OAPCA_API_DATA_URL'),
    api_version='v2')

def setPriorTickerData(tickers):
    # Get Historical data 1 day prior in 1 min increments
    for t in tickers:
        historicalData.update({t: pd.DataFrame(yf.download(tickers = t,period = '1d',interval = '1m').Open)})
        path = str(os.getenv('TICKER_DATA_PATH'))+"/"+str(t)+".xlsx"
        historicalData[t].to_csv(path, index=True)
    run(tickers)

def run(tickers):
    now_UTC = datetime.now(pytz.timezone('America/New_York'))

    while now_UTC.hour < 24:
        testing_count = 0
        for t in tickers:
            testing_count+=1
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
        time.sleep(15)
    print('Markets are currently closed...')
    exit()

    # Calculate the moving average , 5minMA and 15 minMA (check fibonacci seq) concurrent value
    # If buy signal, buy, store this as an actively open position and remove stock from tickers while in position
    # Run the activity check on stock to look for sell signal

def momentumSignal(t):
    orders = api.list_positions()

    # print(any(order.get('symbol') == t for order in orders))
    
    df = pd.read_csv(str(os.getenv('TICKER_DATA_PATH'))+"/"+str(t)+".xlsx", index_col="Datetime")
    # Switched to EMA strategy to reduce price lag
    ema_short = df.ewm(span=5, adjust=False).mean()
    # Taking the difference between the prices and the EMA timeseries
    diff = df.iloc[-1]['Open'] - ema_short.iloc[-1]['Open']
    position = np.sign(diff) * 1/3


    if position == 1/3:
        print('BUYING '+t+' at '+str(df.iloc[-1]['Open']))
        
    else:
        print('Selling '+t+' at '+str(df.iloc[-1]['Open']))                
        # Create sell order

    # Visualization
    # fig = plt.figure()
    # for frame in [df.reset_index(),ema_short.reset_index()]:
    #     plt.plot(frame['Datetime'], frame['Open'])
    # plt.show()
