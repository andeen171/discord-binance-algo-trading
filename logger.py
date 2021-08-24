import discord
from datetime import datetime


def log(msg):
    text = ''.join(msg)
    message = text.replace('\n', ' - ')
    with open('log.txt', 'a') as file:
        file.write(f'{str(datetime.now())} - {message}\n')
        file.close()


def embed(msg):
	# place here the tag you want to mention
    mention = '<@&>'
    title = msg[0]
    description = msg[1]
    return discord.Embed(title=title, description=f'{description}\n {mention}', color=0xffd343)
