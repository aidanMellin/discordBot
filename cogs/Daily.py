from discord.ext import commands, tasks
import discord
import datetime as dt
import asyncio
from dotenv import load_dotenv
import os
from os import getenv
load_dotenv()
OWNER_ID = getenv('OWNER_ID')
CODE_MONKE = 802923855161065495

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.change_daily_status.start()
        self.daily_task.start()
    
    @tasks.loop(hours=24)
    async def change_daily_status(self):
        """
        Updates the bot's status via "Playing game: , based on the day of the week"
        """
        gif_sent = False
        while True:
            channel = self.bot.get_channel(426547798704521216) #ID of #aids channel in my server
            day_status = ["More like monGAY","wait it fucking tueaday .", "💫 Wooback Wednesday","dababy dursday","Gotta get down on friday","FREEDOM!","Fuk. Class tomorrow"] #Status for each dotw
            dotw = dt.datetime.today().weekday() #Day of the week
            await self.bot.change_presence(activity=discord.Game(name=day_status[dotw]))
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
    async def daily_task(self):
        """
        This checks for the completed daily health screen and informs @me via discord ping if it has been completed successfully or not
        """
        while True:
            channel = self.bot.get_channel(CODE_MONKE)
            screen = dt.date.today().strftime('%d-%m-%Y')+".png"
            if(os.path.exists("../dailyHealthBot/screens/"+screen)):
                await channel.send("*Found Daily Health Screen result* <@{owner}>".format(owner=OWNER_ID))
            else:
                await channel.send("*unable to locate today's completed daily health screen* <@{owner}>".format(owner=OWNER_ID))
    
            await asyncio.sleep(60*60*22) #Sleep for 23 hours after notifying to skip the 9am check in (prevents a messaging loop)
            while dt.datetime.now().hour != 9:
                await asyncio.sleep(60*10) #If it's not 9am sleep for 10 minutes and check again
                
def setup(bot):
	bot.add_cog(Daily(bot))