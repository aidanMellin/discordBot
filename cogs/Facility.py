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
    def __init__(self,bot):
        self.bot = bot
        self.avg_activity()

    @commands.command(name='checkGym')
    async def checkGym(self,ctx):
        spots = self.get_fitness()
        self.avg_activity()
        with open('jsonData.json','r') as fp:
            hour = str(dt.datetime.now().hour) #Get the current hour and make it a string
            avgActivity = json.load(fp)['facility'][hour]['avg']
        ctx.channel.send(spots[0],"spots open out of 45, with a typicall average of",avgActivity)

    def get_fitness(self):
        r = requests.get("https://recreation.rit.edu/facilityoccupancy")
        rT = r.text
        occCard = rT.split('<div class="occupancy-card-body">')
        for i in range(len(occCard)):
            if("Fitness Center Occupancy" in occCard[i]):
                finding_Fitness = occCard[i].split("<canvas id=")
        for i in finding_Fitness:
            if "Fitness Center" in i:
                fitnessLevel = [n for n in i.split("</") if "Fitness Center" in n][0]
                space_open = [n.replace('data-occupancy="','').replace('"','') for n in fitnessLevel.split(" ") if "data-occupancy" in n]
        return space_open

    def avg_activity(self):
        '''
        So the idea is to get a constant hourly average of the occupancy at the gym over a period of the open hours (which for now we will just say all day)
        The idea will be to create a JSON object defined by the hours where the contents includes
        Current Average
        #of entries

        to add an entry to the current average, the average will have to be multiplied by the # of entries, have the new value added, and then divide by new value by last recorded # of entries +1
        {hour: %d, avg: %d, entries: %d}
        '''
        while True:
            filePath = "jsonData.json"
            if os.path.exists(filePath):
                with open(filePath, 'r+') as fp:
                    try:
                        JSONData = json.load(fp)['facility'] #Load JSON Object
                        hour = str(dt.datetime.now().hour) #Get the current hour and make it a string
                        curr_value = int(self.get_fitness()[0]) #Get the total number of people in the gym
                        curr_avg = int(JSONData[hour]['avg']) * int(JSONData[hour]['entries']) #Get the total entries in the JSON of the hour so far
                        JSONData[hour]['entries'] = JSONData[hour]['entries'] + 1 #Increase entries by 1
                        JSONData[hour]['avg'] = (curr_avg + curr_value) / int(JSONData[hour]['entries']) #Update the average

                        # print("Current Number of people in the gym: {cv}\nCurrent Avg of people at this hour in the gym: {ca}\nNew calculated average: {js}".format(cv=curr_value,ca=curr_avg,js=JSONData[hour]['avg']))

                    except ValueError:
                        print("No Current JSON Data, beginning new")
                        #This json has to be like '{facility:{ 'hour':{ 'avg': 0, 'entries': 0}}'
                        JSONData = {i:{'avg':0,'entries':0} for i in range(25)}
        
                    fp.seek(0)
                    fp.truncate()

                    json.dump({'facility':JSONData},fp)

                    time.sleep(60*15) #Sleep for 15 minutes
            else:
                os.mknod(filePath)

def setup(bot):
    bot.add_cog(CheckFitness(bot))