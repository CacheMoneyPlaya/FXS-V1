import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv

class AlpacaApi():

    def __init__(self):
        # Load file from the path.
        # load_dotenv('.env')
        # Instantiate the alpaca API for class wide use
        self.api = tradeapi.REST(
            key_id="",
            secret_key="",
            base_url="https://paper-api.alpaca.markets",
            api_version='v2')

    def getAllTickers(self):
        return self.api.list_assets(status=None, asset_class=None)

    def buyOrder(self, t, buy_qty):
        self.api.api.submit_order(t, str(buy_qty), "buy", "market", "day")

    def sellOrder(self, t , sell_qty):
        self.api.submit_order(t, sell_qty, "sell", "market", "day")
