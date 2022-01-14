from binance.client import Client
from binance.streams import ThreadedWebsocketManager
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# %%
client = Client(api_key = api_key, api_secret = secret_key, tld = "com", testnet = True)

# %%
class LongOnlyTrader():
    
    def __init__(self, symbol, start, quote, ratio):
        
        self.symbol = symbol
        self.start = start
        self.quote = quote
        self.ratio = ratio
        grid = list()
        s = start/2
        for i in range(400):
            s *= (1+ratio)
            grid.append(s)
        self.grid = grid
        
    def start_trading(self):
        
        self.twm = ThreadedWebsocketManager()
        self.twm.start()
        
        self.twm.start_symbol_miniticker_socket(callback = self.stream_candles, symbol = self.symbol)
        
    
    def stream_candles(self, msg):
        
        # extract the required items from msg
        time = pd.to_datetime(msg["E"], unit = "ms")
        price = msg["c"]
        self.price = float(price)
    
        print("Time: {} | Price: {}".format(time, price))
        
        status = client.get_account()
        
        coin = status['balances'][-2]['asset']
        free = status['balances'][-2]['free']

        print("Free balance USDT: {}".format(free))      
        
        # in case we want to add a stop trading condition
        #if event_time >= datetime(2022, 11, 4, 9, 55):
         #   self.twm.stop()
          #  if self.position != 0:
           #     order = client.create_order(symbol = self.symbol, side = "SELL", type = "MARKET", quantity = self.units)
            #    self.report_trade(order, "GOING NEUTRAL AND STOP") 
             #   self.position = 0
           # else: 
            #    print("STOP")
        
    
        self.define_strategy()

    def define_strategy(self):
        orders = client.get_open_orders(symbol=self.symbol)
        for i in self.grid:
            if (i*0.9998 <= self.price <= i*1.0002) and (orders==[] or float(orders[-1]['price'])/self.price-1 > self.ratio*2 or self.price/float(orders[-1]['price'])-1 > 0):
                # excecute trades
                self.execute_trades()
                break
            else:    
                pass
       
    def execute_trades(self): 
        # if price in grid and there is not another trade active in the range => BUY and set a LIMIT order
                order = client.create_order(symbol = self.symbol, side = "BUY", type = "MARKET", quoteOrderQty = self.quote)
                self.report_trade(order, "GOING LONG")  
                price = order['fills'][0]['price']
                target = round(float(price)*1.004) 
                qty = order['fills'][0]['qty']
                order = client.create_order(symbol = self.symbol, side = "SELL", type = "LIMIT", timeInForce='GTC', quantity=qty, price=target)
                self.report_trade(order, "SETTING TAKE PROFIT")
        
    def report_trade(self, order, going):
        
        orders = client.get_open_orders(symbol=self.symbol)
        # all_orders = client.get_all_orders(symbol=self.symbol)
        # print trade report
        print(order)
        print(orders)
        # print(all_orders)
        print(2 * "\n" + 100* "-")
       

# %%
trader = LongOnlyTrader(symbol='BTCUSDT',start = 40000, quote = 100, ratio = 0.003)

# %%
trader.start_trading()

# %%
trader.twm.stop()

# %%
balance = {'makerCommission': 0, 'takerCommission': 0, 'buyerCommission': 0, 'sellerCommission': 0, 'canTrade': True, 'canWithdraw': False, 'canDeposit': False, 'updateTime': 1641665383231, 'accountType': 'SPOT', 'balances': [{'asset': 'BNB', 'free': '1000.00000000', 'locked': '0.00000000'}, {'asset': 'BTC', 'free': '0.97778000', 'locked': '0.00245800'}, {'asset': 'BUSD', 'free': '10000.00000000', 'locked': '0.00000000'}, {'asset': 'ETH', 'free': '100.00000000', 'locked': '0.00000000'}, {'asset': 'LTC', 'free': '500.00000000', 'locked': '0.00000000'}, {'asset': 'TRX', 'free': '500000.00000000', 'locked': '0.00000000'}, {'asset': 'USDT', 'free': '10902.62489148', 'locked': '0.00000000'}, {'asset': 'XRP', 'free': '50000.00000000', 'locked': '0.00000000'}], 'permissions': ['SPOT']}

# %%
print(balance['balances'][-2]['asset'])
print(balance['balances'][-2]['free'])

# %%


# %%
float(orders[-1]['price'])

# %%
orders = []

# %%
orders==[]

# %%
price = 43000
ratio = 0.004

# %%
float(orders[-1]['price'])/price-1 > ratio*2

# %%
price/float(orders[-1]['price'])-1 > self.ratio

# %%



