from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_condition import Create
from ibapi.utils import iswrapper
from ibapi.order import *
import threading
import time
import sys

class IBapi(EWrapper, EClient):

    equity = None

    def __init__(self):
         EClient.__init__(self, self)
         self.nextorderId = None

    def start_threading():
        api_thread = threading.Thread(target=run_loop, daemon=True)
        api_thread.start()
        time.sleep(1)

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextorderId = orderId

    def get_next_id(self, num):
        return EClient.reqIds(num)

    def contractCreate(self, symbol):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"

        return contract

    def orderCreate(self, action, qty):
        order = Order()
        order.action = action
        order.orderType = "MKT"
        order.transmit = True
        order.totalQuantity = qty

        return order

    def orderExecution(self, contract, order):
        self.app.placeOrder(self.nextorderId, contract, order)

    def getAllOrders():
        return None

    def getAllPositions():
        return None

    def market_order(self, symbol, qty, action):
        contract = self.contractCreate(symbol)
        order = self.orderCreate(action, qty)
        self.orderExecution(contract, order)

    def openOrder(self, orderId, contract, order, orderState):
        print(order)
        # order.contract = contract
        # self.permId2ord[order.permId] = order

    def accountSummary(self, reqId, account, tag, value, currency):
        self.equity = value

def FX_order(symbol):
	contract = Contract()
	contract.symbol = symbol[:3]
	contract.secType = 'CASH'
	contract.exchange = 'IDEALPRO'
	contract.currency = symbol[3:]
	return contract

def create_contract(symbol, sec_type, exch, prim_exch, curr):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exch
    contract.primaryExch = prim_exch
    contract.currency = curr

    return contract

def create_order(order_type, quantity, action):
    order = Order()
    order.orderType = order_type
    order.totalQuantity = quantity
    order.action = action

    return order

def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 123)
# Start the socket in a thread
time.sleep(2)
# app.reqAllOpenOrders()
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
# app.reqAccountSummary(101, "All", "AvailableFunds")
# time.sleep(3) #Sleep interval to allow time for connection to server

#Check if the API is connected via orderid
# while True:
# 	if isinstance(app.nextorderId, int):
# 		print('connected')
# 		break
# 	else:
# 		print('waiting for connection')
# 		time.sleep(1)

# order = Order()
# order.action = 'BUY'
# order.totalQuantity = 2000
# order.orderType = 'LMT'
# order.lmtPrice = '1.10'

#Place order
aapl_contract = create_contract('AAPL', 'STK', 'SMART', 'SMART' ,'USD')
aapl_order = create_order('MKT', 10, 'BUY')
app.placeOrder(app.nextorderId, aapl_contract, aapl_order)
time.sleep(2)
# print(app.nextorderId)



# print(app.reqAllOpenOrders())

app.disconnect()
