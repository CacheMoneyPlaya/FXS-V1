
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

# ts = TimeSeries(key='J4PU1QWYKNZ1MJZJ', output_format='pandas')
# data, metadata = ts.get_intraday(symbol='DAO', interval='1min')
#
# # Switched to EMA strategy to reduce price lag
# price = pd.DataFrame(data).iloc[::-1]
#
# alpha = (2/(3+1))
# ema_short = price.ewm(alpha=alpha, adjust=False).mean()
#
#
# fig = plt.figure()
# # Visualize
# ema_short['4. close'].plot()
# price['4. close'].plot()
# plt.show()
with open('Strategies/orders.csv', 'a', newline = '') as csvFile:
    csvWriter = csv.writer(csvFile, delimiter = ',')
    csvWriter.writerow(['buy','-1', '4.99', 'TSLA'])
exit()
