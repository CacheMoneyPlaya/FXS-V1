from datetime import datetime
from yahoo_fin import stock_info as si
from datetime import date
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import os
import math
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
    now_UTC = datetime.now(pytz.timezone('America/New_York'))
    # Get Historical data 1 day prior in 1 min increments
    if now_UTC.hour < 24:
        for t in tickers:
            historicalData.update({t: pd.DataFrame(yf.download(tickers = t,period = '1d',interval = '1m').Open)})
            path = str(os.getenv('TICKER_DATA_PATH'))+"/"+str(t)+".xlsx"
            historicalData[t].to_csv(path, index=True)
        run(tickers)
    else:
        print('\033[91m'+'Markets are closed, please run again at 2:30 GMT')

def run(tickers):
    now_UTC = datetime.now(pytz.timezone('America/New_York'))

    while now_UTC.hour < 24:
        for t in tickers:
            path = str(os.getenv('TICKER_DATA_PATH'))+"/"+str(t)+".xlsx"
            # Get stock data, every minute create a new row on top of existing data with new ask
            live_ask = si.get_live_price(t)
            print('\033[92m'+t+' --> '+str(live_ask))
            concurrent_time = datetime.now(pytz.timezone('America/New_York')).strftime("%Y-%m-%d %H:%M:00-05:00")
            # Write the concurrent minute value to existing csv
            with open(path,'a', newline='') as f:
                writer=csv.writer(f)
                writer.writerow([str(concurrent_time), str(live_ask)])
            # Calculate moving averages across Fibonacci time frames
                momentumSignal(t)
        print('\033[91m'+'Analysis Complete')
        if now_UTC.hour == 15 and now_UTC.minute == 30:  
            endDayTradepositions()
        time.sleep(2)
    print('Markets are now closed')    
    exit()

    # Calculate the moving average , 5minMA and 15 minMA (check fibonacci seq) concurrent value
    # If buy signal, buy, store this as an actively open position and remove stock from tickers while in position
    # Run the activity check on stock to look for sell signal

def momentumSignal(t):
    orders = api.list_orders()
    positions = api.list_positions()
    account = api.get_account()

    df = pd.read_csv(str(os.getenv('TICKER_DATA_PATH'))+"/"+str(t)+".xlsx", index_col="Datetime")
    # Switched to EMA strategy to reduce price lag
    ema_short = df.ewm(span=5, adjust=False).mean()
    # Taking the difference between the prices and the EMA timeseries
    diff = df.iloc[-1]['Open'] - ema_short.iloc[-1]['Open']
    position = np.sign(diff) * 1/3
    
    # If we have a buy signal, we have no current pending buy orders and we dont have any open positions buy
    if position == 1/3 and not any(order.symbol == t for order in orders) and not any(position.symbol == t for position in positions):
        # Create buy order with 1/4 of buying power
        print('\033[91m'+'BUYING '+t+' at '+str(df.iloc[-1]['Open']))
        buy_qty = math.ceil((float(account.equity)*(1/4))/(float(df.iloc[-1]['Open'])))
        api.submit_order(t, str(buy_qty), "buy", "market", "day")
    # If we have a sell signal, there are no pending sell orders for that asset and we have a position to sell
    elif position == (-1/3) and any(position.symbol == t for position in positions) and not any(order.symbol == t for order in orders):
        # Create sell order
        print('\033[91m'+'Selling '+t+' at '+str(df.iloc[-1]['Open']))
        sell_qty = next((x.qty for x in orders if x.symbol == t), None)
        api.submit_order(t, str(sell_qty), "sell", "market", "day")

    # Visualization
    # fig = plt.figure()
    # for frame in [df.reset_index(),ema_short.reset_index()]:
    #     plt.plot(frame['Datetime'], frame['Open'])
    # plt.show()

def endDayTradepositions():
    positions = api.list_positions()
    orders = api.list_orders()
    # Sell assets at current price
    for o in orders:
        api.cancel_order(o.order_id)
    for p in positions:
        api.submit_order(p.symbol, p.qty, 'sell', 'market', 'day', limit_price=None, stop_price=None)
    print('\033[91m'+'Orders and positions closed')
    print('Local trading has now ended to preserve strategy integrity')