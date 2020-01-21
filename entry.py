import os
from YahooFinance.yahooFinance import Scraper, YahooData
from datetime import datetime
import time
import Strategies.momentumStrategy as mstrat

class Entry:
    tickers = []

    def __init__(self):
        # Fetch tickers
        self.scraper = Scraper()
        self.fetcher = YahooData()
        self.tickers = self.scraper.getTopPerformers()
        # Iterate through each
        self.regulate(self.tickers)

    def regulate(self, tickers):
        mstrat.setPriorTickerData(tickers)