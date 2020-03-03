
from YahooFinance.yahooFinance import Scraper, YahooData
from datetime import datetime
from dotenv import load_dotenv
from AlpacaAPI.alpacaApi import AlpacaApi
from alpha_vantage.timeseries import TimeSeries
import Strategies.momentumStrategy as mstrat
import matplotlib.pyplot as plt
import os
import math
import pandas as pd
import time
import pytz
import numpy as np
import csv
from yahoo_fin.stock_info import get_live_price

asset_df = pd.read_csv('C:/Users/janva/Documents/Github/FXS-V1/TickerData/PSB.csv', index_col='date')
ema_short = asset_df.ewm(span=2, adjust=False).mean()
ema_long = asset_df.ewm(span=20, adjust=False).mean()

fig = plt.figure()
# Visualize
ema_short['4. close'].plot()
ema_long['4. close'].plot()
plt.show()
exit()
