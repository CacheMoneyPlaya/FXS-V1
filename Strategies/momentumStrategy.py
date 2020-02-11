from datetime import datetime
from AlpacaAPI.alpacaApi import AlpacaApi
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
import os
import math
import pandas as pd
import time
import pytz
import numpy as np
import csv


# Calculate the moving average , 5minMA and 15 minMA (check fibonacci seq) concurrent value
# If buy signal, buy, store this as an actively open position and remove stock from tickers while in position
# Run the activity check on stock to look for sell signal

def momentumSignal(t, api, ts):
    # load_dotenv('.env')
    orders = api.api.list_orders()
    positions = api.api.list_positions()
    account = api.api.get_account()

    asset_df = pd.read_csv('/home/ubuntu/FXS-V1/TickerData/',+t+'.csv', index_col='date')
    ema_short = asset_df.ewm(span=10, adjust=False).mean()

    # Visualize
    # ema_short['4. close'].plot()
    # price['4. close'].plot()
    # plt.show()

    # Taking the difference between the prices and the EMA timeseries
    diff = float(asset_df.iloc[-1]['4. close']) - float(ema_short.iloc[-1]['4. close'])
    position = np.sign(diff)
    # If we have a buy signal, we have no current pending buy orders and we dont have any open positions buy
    if (position == 1 and
        not any(order.symbol == t for order in orders) and
            not any(position.symbol == t for position in positions)):
        # Create buy order with 1/5 of buying power
        print('\033[32m'+'BUYING '+t+' at '+str(asset_df.iloc[-1]['4. close']))
        buy_qty = math.ceil((float(account.equity)*(1/5))/(float(asset_df.iloc[-1]['4. close'])))
        api.api.submit_order(t, str(buy_qty), "buy", "market", "day")
    # If we have a sell signal, there are no pending sell orders for that asset and we have a position to sell
    elif (position == -1 and
        any(position.symbol == t for position in positions) and
            not any(order.symbol == t for order in orders)):
        # Create sell order
        with open('orders.csv', 'a', newline = '') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter = ',')
            csvWriter.writerow(['sell',diff, t])
        print('\033[91m'+'Selling '+t+' at '+str(asset_df.iloc[-1]['4. close']))
        sell_qty = next((x.qty for x in positions if x.symbol == t), None)
        api.api.submit_order(t, sell_qty, "sell", "market", "day")
    else:
        print('\033[91m' + 'No trades viable' + ' @ ' + t)
