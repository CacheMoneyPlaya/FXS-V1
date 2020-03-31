import requests
import pandas as pd
import numpy as np
import yfinance as yf
import csv
from bs4 import BeautifulSoup
from AlpacaAPI.alpacaApi import AlpacaApi
from alpha_vantage.timeseries import TimeSeries
from Spreadsheets.csvHandler import csvHandler as csv

class Scraper:

    def __init__(self):
        self.tickers = []
        self.available = []
        self.mapper = csv()

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
        for a in assets:
            if a.contents[0] in self.available and len(self.tickers) < 2:
                self.tickers.append(a.contents[0])
        # Set the inital historical data to be used for the days spread
        for t in self.tickers:
            data, metadata = ts.get_intraday(symbol=t, interval='1min')
            transformed_data = pd.DataFrame(data).iloc[::-1]
            self.mapper.initalHistoricData(t, transformed_data)

        return self.tickers

class YahooData:

    def getTickerData(self, ticker):
        return yf.Ticker(ticker)
