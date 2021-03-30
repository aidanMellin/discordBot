import asyncio
import datetime as dt
import discord
import os

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
    change_daily_status.start()
    daily_task.start()

@tasks.loop(hours=24)    
async def change_daily_status():
    """
    Updates the bot's status via "Playing game: , based on the day of the week"
    """
    gif_sent = False
    while True:
        channel = bot.get_channel(426547798704521216) #ID of #aids channel in my server
        day_status = ["More like monGAY","wait it fucking tueaday .", "<:dizzy:> Wooback Wednesday","dababy dursday","Gotta get down on friday","FREEDOM!","Fuk. Class tomorrow"] #Status for each dotw
        dotw = dt.datetime.today().weekday() #Day of the week
        await bot.change_presence(activity=discord.Game(name=day_status[dotw]))
        #await bot.get_channel(CODE_MONKE).send("Daily status updated")
        if not gif_sent:
            if dotw == 3:
                await channel.send(file=discord.File('media/gif/dababy.gif'))
            if dotw == 4:
                await channel.send(file=discord.File('media/gif/friday.gif'))
            gif_sent = True

        await asyncio.sleep(60*60*3) #Sleep for 3 hours
        if dotw != dt.datetime.today().weekday(): #If the day changed after waiting for 3 hours
            gif_sent = False

@tasks.loop(hours=24)            
async def daily_task():
    """
    This checks for the completed daily health screen and informs @me via discord ping if it has been completed successfully or not
    """
    while True:
        channel = bot.get_channel(CODE_MONKE)
        screen = dt.date.today().strftime('%d-%m-%Y')+".png"
        if(os.path.exists("../dailyHealthBot/screens/"+screen)):
            await channel.send("*Found Daily Health Screen result* <@{owner}>".format(owner=OWNER_ID))
        else:
            await channel.send("*unable to locate today's completed daily health screen* <@{owner}>".format(owner=OWNER_ID))

        await asyncio.sleep(60*60) #Sleep for an hour after notifying to skip the 9am check in (prevents a messaging loop)
        while dt.datetime.now().hour != 9:
            await asyncio.sleep(60*10) #If it's not 9am sleep for 10 minutes and check again

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