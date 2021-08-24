import math
from math import floor
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException


class BinanceTradeBot:

    def __init__(self, key, secret, crypto, info):
        self.client = Client(key, secret)
        self.status = info['status']
        self.crypto = crypto
        self.last_sell = info['last_sell']
        self.last_buy = info['last_buy']
        self.terms = info['terms']
        self.price = float(self.client.get_symbol_ticker(symbol=f"{crypto}BUSD")['price'])
        # Data for MA lines
        self.data = self.client.get_historical_klines(f"{crypto}BUSD", self.client.KLINE_INTERVAL_1HOUR,
                                                      f"{info['terms'][1]} hours ago UTC")

    # Write here the method you want the bot to follow and determine when buy or sell
    def get_status(self):
        """
        Uses especifics MA lines to determine golden cross(buy) and death cross(sell)
        """
        short_term = self.terms[0]
        long_term = self.terms[1]
        long_data = 0
        short_data = 0
        loop = len(self.data) - 1
        for x in range(loop):
            long_data += float(self.data[x][4])
            if x >= ((short_term - loop) * -1):
                short_data += float(self.data[x][4])
        long = long_data / long_term
        short = short_data / short_term
        if long > short and self.status != 'waiting':
            self.status = 'SELL'
            return True
        elif short > long and self.status != 'holding':
            self.status = 'BUY'
            return True
        return False

    def create_order(self):
        """
        Build an order object with the especific parameters and return it
        """
        step_size = self.client.get_symbol_info(f'{self.crypto}BUSD')['filters'][2]['stepSize']
        precision = int(round(-math.log(float(step_size), 10), 0))
        order = {'time': str(datetime.now())}
        if self.status == "SELL":
            order['type'] = "SELL"
            order['quantity'] = round(float(self.client.get_asset_balance(asset=self.crypto)['free']), precision)
            order['value'] = round(order['quantity'] * self.price, 2)
            self.last_sell = order
            self.status = 'waiting'
        else:
            order['type'] = "BUY"
            order['value'] = self.last_sell['value']
            order['quantity'] = round(floor((order['value'] / self.price) * 1000000) / 1000000, precision)
            self.last_buy = order
            self.status = 'holding'
        return order

    def trade(self, order):
        """
        Do a trade based on the order object
        """
        s = order['type']
        q = order['quantity']
        v = order['value']
        try:
            # Change to create_order if you want it to spend your currency
            self.client.create_test_order(symbol=f'{self.crypto}BUSD', side=s, type='MARKET', quantity=q)
        except BinanceAPIException as error:
            return ["Failed to do a '{s}' order in {self.crypto}\n",
                    f"Error code: {error.status_code}\n{error.message}"]
        return [f"Sucessfully did a '{s}' in {self.crypto}",
                f"Trade of {q} for ${v}"]
