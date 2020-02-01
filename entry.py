from YahooFinance.yahooFinance import Scraper, YahooData
from datetime import datetime
from dotenv import load_dotenv
from AlpacaAPI.alpacaApi import AlpacaApi
from alpha_vantage.timeseries import TimeSeries
import Strategies.momentumStrategy as mstrat
import os
import math
import pandas as pd
import time
import pytz
import numpy as np

class Entry:
    tickers = []
    api = AlpacaApi()
    ts = TimeSeries(key='J4PU1QWYKNZ1MJZJ', output_format='pandas')

    def __init__(self):
        load_dotenv('.env')
        # Fetch tickers
        scraper = Scraper()
        tickers = scraper.getTopPerformers()
        # Iterate through each
        self.setTickerFocus(tickers)

    def setTickerFocus(self, tickers):
        now_UTC = datetime.now(pytz.timezone('America/New_York'))
        # Get Historical data 1 day prior in 1 min increments
        if now_UTC.hour < 16:
            self.run(tickers)
        else:
            print('\033[91m'+'Markets are closed, please run again at 2:30 GMT')

    def run(self, tickers):
        now_UTC = datetime.now(pytz.timezone('America/New_York'))

        while now_UTC.hour < 16:
            for t in tickers:
                #Can theoretically set the applicable strats here
                mstrat.momentumSignal(t, self.api, self.ts)

            print('\033[32m'+ '--------- ' +'Round Complete' + ' ---------')
            time.sleep(60)
        self.endDayTradepositions()
        print('Markets are now closed')    
        exit()
    
    def endDayTradepositions(self):
        positions = self.api.api.list_positions()
        orders = self.api.api.list_orders()
        # Sell assets at current price
        for o in orders:
            self.api.api.cancel_order(o.order_id)
        for p in positions:
            self.api.api.submit_order(p.symbol, p.qty, 'sell', 'market', 'day')
        print('\033[91m'+'Orders and positions closed')
        print('Local trading has now ended to preserve strategy integrity')