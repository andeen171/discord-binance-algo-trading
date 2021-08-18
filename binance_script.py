import math
import yaml
from math import floor
from datetime import datetime
from binance.exceptions import BinanceAPIException

# loads api credentials
with open('auth.yml') as yml:
    auth = yaml.load(yml, Loader=yaml.FullLoader)
    api_key = auth['binance_api']
    api_secret = auth['binance_secret']


class BinanceTradeBot:

    def __init__(self, client, code, jason, preco, dados):
        self.client = client
        self.status = jason['status']
        self.crypto = code
        self.last_sell = jason['last_sell']
        self.last_buy = jason['last_buy']
        self.price = preco
        self.data = dados

    def get_status(self):
        long_term = 0
        short_term = 0
        for x in range(len(self.data) - 1):
            long_term += float(self.data[x][4])
            if x >= 6:
                short_term += float(self.data[x][4])
        long = long_term / 12
        short = short_term / 6
        if long > short and self.status != 'waiting':
            self.status = 'SELL'
        elif short > long and self.status != 'holding':
            self.status = 'BUY'
        return self.status

    def get_quantity(self):
        step_size = self.client.get_symbol_info(f'{self.crypto}BUSD')['filters'][2]['stepSize']
        precision = int(round(-math.log(float(step_size), 10), 0))
        if self.status == 'BUY':
            value = self.last_sell['value']
            self.status = 'holding'
            return round(floor((value / self.price) * 1000000) / 1000000, precision)
        elif self.status == 'SELL':
            return round(float(self.client.get_asset_balance(asset=self.crypto)['free']), precision)

    def place_order(self):
        quantity = self.get_quantity()
        try:
            self.client.create_test_order(symbol=f'{self.crypto}BUSD', side=self.status,
                                          type='MARKET', quantity=quantity)
        except BinanceAPIException as error:
            print(error.status_code)
            print(error.message)
            return f"Failed to place an '{self.status}' order of {quantity} {self.crypto}"
        else:
            value = round(quantity * self.price, 2)
            order = {'amount': quantity, 'value': value, 'time': str(datetime.now())}
            if self.status == 'BUY':
                before = self.last_sell['amount']
                margin = round(((quantity - before) / before) * 100, 2)
                self.last_buy = order
            else:
                before = self.last_buy['value']
                margin = round(((value - before) / before) * 100, 2)
                self.last_sell = order
            return f"Sucessfully did a '{self.status}' trade of {quantity} {self.crypto}\n" \
                   f"with aprox. {str(margin)}% profit"
