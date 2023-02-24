import discord
import asyncio
import os
import aiologger
from dotenv import load_dotenv
from db.connection import get_db_engine

load_dotenv()
logger = aiologger.Logger.with_default_handlers(level=10)
intents = discord.Intents.default()
intents.message_content = True
mention = '<@&>'


# title = msg[0]
# description = msg[1]
# discord.Embed(title=title, description=f'{description}\n {mention}', color=0xffd343)


async def main():
    db_engine, db_session = await get_db_engine()
    await db_engine.dispose()


if __name__ == '__main__':
    client = MyClient(intents=intents)
    client.run(os.environ.get('DISCORD_API'))
    asyncio.run(main())
