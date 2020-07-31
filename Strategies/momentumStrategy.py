from datetime import datetime
from AlpacaAPI.alpacaApi import AlpacaApi
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
from Spreadsheets import csvHandler as ch
import pandas as pd
import numpy as np
import os
import math
import time
import pytz
import csv

# Calculate the moving average , 5minMA and 15 minMA (check fibonacci seq) concurrent value
# If buy signal, buy, store this as an actively open position and remove stock from tickers while in position
# Run the activity check on stock to look for sell signal

def momentumSignal(t, api, ts, ch):
    #Fetch a list of orders, positions, account data and asset dataframe
    orders = api.api.list_orders()
    positions = api.api.list_positions()
    account = api.api.get_account()
    asset_df = ch.read_tickers(t)
    #Create a df for both ema short and long for comparason
    ema_short = asset_df.ewm(span=2, adjust=False).mean()
    ema_long = asset_df.ewm(span=20, adjust=False).mean()
    # Taking the difference between the prices and the EMA timeseries
    diff = float(ema_short.iloc[-1]['4. close']) - float(ema_long.iloc[-1]['4. close'])
    position = np.sign(diff)
    prior_diff = float(ema_short.iloc[-2]['4. close']) - float(ema_long.iloc[-2]['4. close'])
    prior_position = np.sign(prior_diff)
    # If we have a buy signal, we have no current pending buy orders and we dont have any open positions buy
    # and have recently cut the moving average
    if (is_buy(position, prior_position, orders, positions)):
        # Create buy order with 1/5 of buying power
        print('\033[32m'+'BUYING '+t+' at '+str(asset_df.iloc[-1]['4. close']))
        buy_qty = math.ceil((float(account.equity)*(1/5))/(float(asset_df.iloc[-1]['4. close'])))
        # Make a buy order
        self.api.api.market_order(t, buy_qty, 'BUY')
    # If we have a sell signal, there are no pending sell orders for that asset and we have a position to sell
    elif (is_sell(position, prior_position, orders, positions)):
        # Create sell order with all volume we have with asset "t"
        print('\033[91m'+'Selling '+t+' at '+str(asset_df.iloc[-1]['4. close']))
        sell_qty = next((x.qty for x in positions if x.symbol == t), None)
        # Make a sell order
        self.api.api.market_order(t, sell_qty, 'SELL')
    else:
        print('\033[91m' + 'No trades viable' + ' @ ' + t)

def is_buy(position, prior_position, orders, positions):
    return (position == 1 and
                prior_position == -1 and
                    not any(order.symbol == t for order in orders) and
                        not any(position.symbol == t for position in positions))

def is_sell(position, prior_position, orders, positions):
    return (position == -1 and
                prior_position == 1 and
                    any(position.symbol == t for position in positions) and
                        not any(order.symbol == t for order in orders))
