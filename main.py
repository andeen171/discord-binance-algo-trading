import json
import yaml
import asyncio
import discord
from logger import log, embed
from binance_script import BinanceTradeBot

data = "data.json"
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
            with open(data, 'r') as file:
                config = json.load(file)
                for crypto, info in config.items():
                    bot = BinanceTradeBot(api_key, api_secret, crypto, info)
                    if bot.get_status():
                        order = bot.create_order()
                        message = bot.trade(order)
                        log(message)
                        await channel.send(embed=embed(message))
                    info['status'] = bot.status
                    info['last_buy'] = bot.last_buy
                    info['last_sell'] = bot.last_sell
            with open(data, 'w') as file:
                save = json.dumps(config, indent=4)
                file.write(save)
            await asyncio.sleep(300)


if __name__ == '__main__':
    dc = MyClient()
    dc.run(discord_key)
