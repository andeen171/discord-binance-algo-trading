import discord
import yaml

with open('auth.yml') as yml:
    auth = yaml.load(yml, Loader=yaml.FullLoader)
    api_key = auth['binance_api']
    api_secret = auth['binance_secret']
    discord_key = auth['discord_apikey']


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def log(self, message):
        channel = self.get_channel(877341571173986325)
        await channel.send(message)


dc = MyClient()
dc.run(discord_key)
