
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

ts = TimeSeries(key='J4PU1QWYKNZ1MJZJ', output_format='pandas')
data, metadata = ts.get_intraday(symbol='RL', interval='1min')

# Switched to EMA strategy to reduce price lag
price = pd.DataFrame(data)
alpha = (2/(3+1))
ema_short = pd.DataFrame(data).ewm(alpha=alpha, adjust=False).mean().shift(-3)


fig = plt.figure()
# Visualize
ema_short['4. close'].plot()
price['4. close'].plot()
plt.show()
exit()
