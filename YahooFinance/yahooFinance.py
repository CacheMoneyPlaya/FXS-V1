import requests
import pandas as pd
import numpy as np
import yfinance as yf
import csv
from bs4 import BeautifulSoup
from AlpacaAPI.alpacaApi import AlpacaApi
from alpha_vantage.timeseries import TimeSeries

class Scraper:

    tickers = []
    available = []

    def getTopPerformers(self):
        url = "https://finance.yahoo.com/gainers"
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        assets = soup.find_all('a', attrs={"class":"Fw(600)"})
        api = AlpacaApi()
        ts = TimeSeries(key='J4PU1QWYKNZ1MJZJ', output_format='pandas')
        availableTickers = api.getAllTickers()

        # Filter all of the day's available symbols
        for a in availableTickers:
            self.available.append(a.symbol)

        # Create a list of 3 of the top performing daily symbols
        for i in assets:
            if i.contents[0] in self.available and len(self.tickers) < 3:
                self.tickers.append(i.contents[0])

        for i in self.tickers:
            data, metadata = ts.get_intraday(symbol=i, interval='1min')
            transformed_data = pd.DataFrame(data).iloc[::-1]
            transformed_data.to_csv('/home/ubuntu/FXS-V1/TickerData'+i+'.csv')
        return self.tickers

class YahooData:

    def getTickerData(self, ticker):
        return yf.Ticker(ticker)
