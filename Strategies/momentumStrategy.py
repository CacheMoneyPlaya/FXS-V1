from datetime import datetime
from yahoo_fin import stock_info as si
from datetime import date
from dotenv import load_dotenv
from AlpacaAPI.alpacaApi import AlpacaApi
from alpha_vantage.timeseries import TimeSeries
import os
import math
import pandas as pd
import time
import pytz
import numpy as np
import yfinance as yf
import csv
import matplotlib.pyplot as plt 
import json


load_dotenv('.env')

api = AlpacaApi()
ts = TimeSeries(key='J4PU1QWYKNZ1MJZJ', output_format='pandas')

def setPriorTickerData(tickers):
    now_UTC = datetime.now(pytz.timezone('America/New_York'))
    # Get Historical data 1 day prior in 1 min increments
    if now_UTC.hour < 24:
        run(tickers)
    else:
        print('\033[91m'+'Markets are closed, please run again at 2:30 GMT')

def run(tickers):
    now_UTC = datetime.now(pytz.timezone('America/New_York'))

    while now_UTC.hour < 16:
        for t in tickers:
                momentumSignal(t)

        print('\033[32m'+ '--------- ' +'Round Complete' + ' ---------')
        if now_UTC.hour == 15 and now_UTC.minute == 30:  
            endDayTradepositions()
        time.sleep(60)
    print('Markets are now closed')    
    exit()

    # Calculate the moving average , 5minMA and 15 minMA (check fibonacci seq) concurrent value
    # If buy signal, buy, store this as an actively open position and remove stock from tickers while in position
    # Run the activity check on stock to look for sell signal

def momentumSignal(t):
    orders = api.api.list_orders()
    positions = api.api.list_positions()
    account = api.api.get_account()
    data, metadata = ts.get_intraday(symbol=t, interval='1min')
    # Switched to EMA strategy to reduce price lag
    price = pd.DataFrame(data)
    ema_short = pd.DataFrame(data).ewm(span=4, adjust=False).mean().shift(-4)
    # Visualize
    # ema_short['4. close'].plot()
    # price['4. close'].plot()
    # plt.show()
    # Taking the difference between the prices and the EMA timeseries
    diff = float(price.iloc[0]['4. close']) - float(ema_short.iloc[0]['4. close'])
    position = np.sign(diff) * 1/3
    # If we have a buy signal, we have no current pending buy orders and we dont have any open positions buy
    if math.isclose(position,1/3, abs_tol=1e-8) and not any(order.symbol == t for order in orders) and not any(position.symbol == t for position in positions):
        # Create buy order with 1/4 of buying power
        print('\033[32m'+'BUYING '+t+' at '+str(price.iloc[0]['4. close']))
        buy_qty = math.ceil((float(account.equity)*(1/4))/(float(price.iloc[0]['4. close'])))
        api.api.submit_order(t, str(buy_qty), "buy", "market", "day")
    # If we have a sell signal, there are no pending sell orders for that asset and we have a position to sell
    elif math.isclose(position,-1/3, abs_tol=1e-8) and any(position.symbol == t for position in positions) and not any(order.symbol == t for order in orders):
        # Create sell order
        print('\033[91m'+'Selling '+t+' at '+str(price.iloc[0]['4. close']))
        sell_qty = next((x.qty for x in positions if x.symbol == t), None)
        api.api.submit_order(t, sell_qty, "sell", "market", "day")
    else:
        print('\033[91m' + 'No trades viable' + ' @ ' + t)



def endDayTradepositions():
    positions = api.api.list_positions()
    orders = api.api.list_orders()
    # Sell assets at current price
    for o in orders:
        api.api.cancel_order(o.order_id)
    for p in positions:
        api.api.submit_order(p.symbol, p.qty, 'sell', 'market', 'day')
    print('\033[91m'+'Orders and positions closed')
    print('Local trading has now ended to preserve strategy integrity')