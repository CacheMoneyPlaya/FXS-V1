import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv

class AlpacaApi():

    def __init__(self):
        # Load file from the path.
        load_dotenv('.env')
        # Instantiate the alpaca API for class wide use
        self.api = tradeapi.REST(
            os.getenv('APCA_API_KEY_ID'),
            os.getenv('APCA-API-SECRET-KEY'),
            os.getenv('OAPCA_API_DATA_URL'),
            api_version='v2')
    
    def getAllTickers(self):
        return self.api.list_assets(status=None, asset_class=None)
    
    def getTickerData(self):
        print('Getting ticker data')