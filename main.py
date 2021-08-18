import json
import yaml
import discord
import asyncio
from time import sleep
from binance_script import BinanceTradeBot
from binance.client import Client


with open('auth.yml') as yml:
    auth = yaml.load(yml, Loader=yaml.FullLoader)
    api_key = auth['binance_api']
    api_secret = auth['binance_secret']
    discord_key = auth['discord_apikey']


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.binance_script())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def binance_script(self):
        await self.wait_until_ready()
        channel = self.get_channel(877341571173986325)  # channel ID goes here
        while True:
            with open('data.json', 'r') as file:
                config = json.load(file)
                api = Client(api_key, api_secret)
                for crypto, info in config.items():
                    price = float(api.get_symbol_ticker(symbol=f"{crypto}BUSD")['price'])
                    data = api.get_historical_klines(f"{crypto}BUSD", api.KLINE_INTERVAL_1HOUR,
                                                     "13 hours ago UTC")
                    bot = BinanceTradeBot(api, crypto, info, price, data)
                    bot.get_status()
                    print(bot.status)
                    if bot.status == 'BUY':
                        await channel.send(bot.place_order())
                        info['status'] = 'holding'
                        info['last_buy'] = bot.last_buy
                    elif bot.status == 'SELL':
                        await channel.send(bot.place_order())
                        info['status'] = 'waiting'
                        info['last_sell'] = bot.last_sell
                    else:
                        await channel.send(f'No trades done for {crypto}')
            with open('data.json', 'w') as file:
                save = json.dumps(config, indent=4)
                file.write(save)
            await channel.send('now sleeping for 15min...')
            sleep(900)
            await asyncio.sleep(60)


dc = MyClient()
dc.run(discord_key)
