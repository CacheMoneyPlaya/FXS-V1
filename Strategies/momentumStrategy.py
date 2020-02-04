from datetime import datetime
from AlpacaAPI.alpacaApi import AlpacaApi
from alpha_vantage.timeseries import TimeSeries
import os
import math
import pandas as pd
import time
import pytz
import numpy as np


# Calculate the moving average , 5minMA and 15 minMA (check fibonacci seq) concurrent value
# If buy signal, buy, store this as an actively open position and remove stock from tickers while in position
# Run the activity check on stock to look for sell signal

def momentumSignal(t, api, ts):
    orders = api.api.list_orders()
    positions = api.api.list_positions()
    account = api.api.get_account()
    data, metadata = ts.get_intraday(symbol=t, interval='1min')

    # Switched to EMA strategy to reduce price lag with alpha for further log accuracy
    price = pd.DataFrame(data)
    alpha = 5
    ema_short = pd.DataFrame(data).ewm(span=alpha, adjust=False).mean().shift(-5)

    # Visualize
    # ema_short['4. close'].plot()
    # price['4. close'].plot()
    # plt.show()

    # Taking the difference between the prices and the EMA timeseries
    diff = float(price.iloc[0]['4. close']) - float(ema_short.iloc[0]['4. close'])
    position = np.sign(diff)

    # Scenario where the momentum doesn't react in time to place a correct sell we force liquidation:
    if (any(position.symbol == t for position in positions) and 
            float(price.iloc[0]['4. close']) < float(next((p.qty for p in positions if p.symbol == t), None))):
        position = -1
    
    # If we have a buy signal, we have no current pending buy orders and we dont have any open positions buy
    if (position == 1 and 
        not any(order.symbol == t for order in orders) and 
            not any(position.symbol == t for position in positions)):
        # Create buy order with 1/4 of buying power
        print('\033[32m'+'BUYING '+t+' at '+str(price.iloc[0]['4. close']))
        buy_qty = math.ceil((float(account.equity)*(1/4))/(float(price.iloc[0]['4. close'])))
        api.api.submit_order(t, str(buy_qty), "buy", "market", "day")
    # If we have a sell signal, there are no pending sell orders for that asset and we have a position to sell
    elif (position == -1 and 
        any(position.symbol == t for position in positions) and 
            not any(order.symbol == t for order in orders)):
        # Create sell order
        print('\033[91m'+'Selling '+t+' at '+str(price.iloc[0]['4. close']))
        sell_qty = next((x.qty for x in positions if x.symbol == t), None)
        api.api.submit_order(t, sell_qty, "sell", "market", "day")
    else:
        print('\033[91m' + 'No trades viable' + ' @ ' + t)
