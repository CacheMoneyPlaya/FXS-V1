import requests
import numpy as np
import yfinance as yf
from bs4 import BeautifulSoup
from AlpacaAPI.alpacaApi import AlpacaApi

class Scraper:

    tickers = []
    available = []

    def getTopPerformers(self):
        url = "https://finance.yahoo.com/gainers"
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        assets = soup.find_all('a', attrs={"class":"Fw(600)"})
        api = AlpacaApi()
        availableTickers = api.getAllTickers()

        # Filter all of the day's available symbols
        for a in availableTickers:
            self.available.append(a.symbol)

        # Create a list of 3 of the top performing daily symbols
        for i in assets:
            if i.contents[0] in self.available and len(self.tickers) < 3:
                self.tickers.append(i.contents[0])
        return self.tickers

class YahooData:

    def getTickerData(self, ticker):
        return yf.Ticker(ticker)