from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time
from overrides import overrides
import pandas as pd

#Orders -> DONE
#Positions -> DONE
#Current liquidity -> DONE

class InteractiveBrokersAPI(EWrapper, EClient):

    equity = None

    def __init__(self):
         EClient.__init__(self, self)
         self.nextOrderId = None
         self.positions = pd.DataFrame([], columns = ['Symbol', 'Quantity'])
         self.orders = pd.DataFrame([], columns = ['Symbol', 'Quantity', 'Action'])

    def start_threading(self):
        api_thread = threading.Thread(target=run_loop, daemon=True)
        api_thread.start()
        time.sleep(1)

    def reset_data_frame(self, dataframe):
        dataframe.index = self.orders.index + 1
        return dataframe.sort_index()

    @overrides
    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)
        self.orders.loc[-1] = [contract.symbol, order.totalQuantity, order.action]
        self.orders = self.reset_data_frame(self.orders)

    @overrides
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextOrderId = orderId

    @overrides
    def position(self, account, contract, position, avgCost):
        super().openOrder(account, contract, position, avgCost)
        if account == 'DU2650196':
            self.positions.loc[-1] = [contract.symbol, position]
            self.positions = self.reset_data_frame(self.positions)


    def get_next_id(self, num):
        return EClient.reqIds(num)

    def orderExecution(self, contract, order):
        self.app.placeOrder(self.nextOrderId, contract, order)

    def market_order(self, symbol, qty, action):
        contract = self.contractCreate(symbol)
        order = self.orderCreate(action, qty)
        self.orderExecution(contract, order)

    @overrides
    def accountSummary(self, reqId, account, tag, value, currency):
        if account == 'DU2650196':
            self.equity = value

    def create_contract(self, symbol):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.primaryExch = 'SMART'
        contract.currency = 'USD'

        return contract

    def create_order(self, quantity, action):
        order = Order()
        order.orderType = 'MKT'
        order.totalQuantity = quantity
        order.action = action

        return order


def run_loop():
	app.run()

app = InteractiveBrokersAPI()
app.connect('127.0.0.1', 7497, 123)
# Start the socket in a thread
time.sleep(1)
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
# app.reqAllOpenOrders()
app.reqPositions()
time.sleep(1)
print(app.positions)
# app.reqAccountSummary(101, "All", "AvailableFunds")
# time.sleep(3) #Sleep interval to allow time for connection to server
#
#Place order
# aapl_contract = app.create_contract('AAPL')
# aapl_order = app.create_order(10, 'BUY')
# app.placeOrder(app.nextOrderId, aapl_contract, aapl_order)
time.sleep(2)

app.disconnect()
