from asyncio import sleep
from discord import Client


class MyClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = None

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.binance_script())

    async def binance_script(self):
        await self.wait_until_ready()
        # channel = self.get_channel(877341571173986325)  # channel ID goes here
        # message = 'a'
        # logger.info(message)
        # await channel.send(embed=embed(message))
        await sleep(300)
