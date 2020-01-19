import os
from Scraping.scraper import Scraper
from datetime import datetime

class Entry:
    tickers = []

    def __init__(self):
        # Fetch tickers
        self.scraper = Scraper()
        self.tickers = self.scraper.getTopPerformers()
        # Iterate through each
        print(self.tickers)
        exit()
        self.regulate(self.tickers)

    def regulate(self, tickers):
        now_UTC = datetime.utcnow()
        while True:
            if now_UTC.hour < 24:
                for t in enumerate(self.tickers):
                    # Get stock data
                    print(t)
                    # Apply strategies
                    # Sleep for 1 minute
            else:
                # Trading hours are over
                exit()