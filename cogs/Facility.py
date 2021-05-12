import requests
import discord
from discord.ext import commands, tasks
import asyncio
import json
import simplejson
from json import JSONEncoder
import os
import datetime as dt
import time


class CheckFitness(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        #self.avg_activity.start()
        self.filePath = "jsonData.json"

    @commands.command(name='checkGym')
    async def checkGym(self, ctx):
        """
        Prints the number of people currently at the gym and the average number of people typically there at this time

        Usage:
            **~checkGym**
        Args:
            ctx: Discord Context Object
        """
        spots = self.get_fitness()
        with open(self.filePath, 'r') as fp:
            # Get the current hour and make it a string
            hour = str(dt.datetime.now().hour)
            avgActivity = json.load(fp)['facility'][hour]['avg']
        rtn = " {spots_used} spots being used out of 45, with a typical average of {avg}".format(
            spots_used=spots[0], avg=avgActivity)
        await ctx.channel.send(rtn)

    def get_fitness(self):
        """Using HTML requests (because the page is designed terribly) get the number of people currently at the gym

        Returns:
            [int]: number of people currently at the gym
        """
        r = requests.get("https://recreation.rit.edu/facilityoccupancy")
        rT = r.text
        occCard = rT.split('<div class="occupancy-card-body">')
        for i in range(len(occCard)):
            if("Fitness Center Occupancy" in occCard[i]):
                finding_Fitness = occCard[i].split("<canvas id=")
        for i in finding_Fitness:
            if "Fitness Center" in i:
                fitnessLevel = [n for n in i.split(
                    "</") if "Fitness Center" in n][0]
                space_used = [n.replace('data-occupancy="', '').replace('"', '')
                              for n in fitnessLevel.split(" ") if "data-occupancy" in n]
        return space_used

    @tasks.loop()
    async def avg_activity(self):
        """This is a way of accessing the driver avg_activity tool such that the JSON file can be read after being edited 
        (if this was one program, the file ) would not be closed until the method ends.
        """
        while True:
            self.avg_activity_data()
            await asyncio.sleep(60*15)

    def avg_activity_data(self):
        """
        Determine current number of people at the gym, read the JSON and update the average accordingly
        """
        if os.path.exists(self.filePath):
            with open(self.filePath, 'r') as fp:
                try:
                    # Load JSON Object
                    allJSON = json.load(fp)
                    keywordJSON = allJSON['keywords']
                    todoJSON = allJSON['todo']

                    JSONData = allJSON['facility']
                    # Get the current hour and make it a string
                    hour = str(dt.datetime.now().hour)
                    # Get the total number of people in the gym
                    curr_value = int(self.get_fitness()[0])
                    # Get the total entries in the JSON of the hour so far
                    curr_avg = int(JSONData[hour]['avg']) * \
                        int(JSONData[hour]['entries'])
                    # Increase entries by 1
                    JSONData[hour]['entries'] = JSONData[hour]['entries'] + 1
                    JSONData[hour]['avg'] = (
                        curr_avg + curr_value) / int(JSONData[hour]['entries'])  # Update the average

                except ValueError:
                    print("No Current JSON Data, beginning new")
                    # This json has to be like '{facility:{ 'hour':{ 'avg': 0, 'entries': 0}}'
                    JSONData = {i:
                                {'avg': 0,
                                 'entries': 0} for i in range(25)}

            with open(self.filePath, 'w') as f:
                # Dump the data
                json.dump(
                    {'facility': JSONData, 'keywords': keywordJSON, 'todo': todoJSON}, f)
        else:
            os.mknod(filePath)


def setup(bot):
    """Initialize the bot

    Args:
        bot Discord Bot object: Bot object to have the cog added to
    """
    bot.add_cog(CheckFitness(bot))


if __name__ == "__main__":
    cf = CheckFitness(None)
    cf.checkGym(None)
