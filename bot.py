import asyncio
import discord
import os
import datetime as dt

from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv, listdir

"""
Load all variables (Bot guild and bot token))
"""
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
GUILD = getenv('DISCORD_GUILD')
OWNER_ID = getenv('OWNER_ID')
MINER_ID = getenv('MY_ID')
CODE_MONKE = 802923855161065495

cogs_dir = "cogs"

bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready():
    guild = None
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        f"Today's Date is: "+dt.date.today().strftime('%d-%m-%Y')
    )

if __name__=='__main__':
	"""Loads the cogs from the `./cogs` folder.
	Notes:
		The cogs are .py files.
		The cogs are named in this format `{cog_dir}.{cog_filename_without_extension}`_.
		"""
	for cog in listdir('./cogs'):
		if cog.endswith('.py') == True:
			bot.load_extension(f'cogs.{cog[:-3]}')

bot.run(TOKEN)
