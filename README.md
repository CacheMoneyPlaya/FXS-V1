```
_____ __  __ ____         __     __ _      _     _       ____   ___   
|  ___|\ \/ // ___|        \ \   / // |    / \   | |     / ___| / _ \  
| |_    \  / \___ \  _____  \ \ / / | |   / _ \  | |    | |  _ | | | |
|  _|   /  \  ___) ||_____|  \ V /  | |  / ___ \ | |___ | |_| || |_| |  
|_|    /_/\_\|____/           \_/   |_| /_/   \_\|_____| \____| \___/  
```
- Algo trading bot for all US stock assets
- Mainly uses SMA strat with 1,2,3 ... thinking of 1,2, 5 instead
- Only trades per day, closes all positions end of trading hours
- Must specify some local env variables prior:

 + APCA_API_KEY_ID
 + APCA-API-SECRET-KEY
 + OAPCA_API_DATA_URL=https://paper-api.alpaca.markets
 + CSV_LOCATION
 
 For intiation of venv refer to : https://docs.python.org/3/library/venv.html
 To install required packages run `pip install -r requirements.txt`
 
2/08/20 - Began a few days ago integrating Interactive Brokers API/Workstation for more profeessional use.
