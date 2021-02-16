#!/usr/bin/python3
# bot.py

#Standard packages
import asyncio
import datetime as dt
import os
import random as r
import string

#Custom packages
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from minersRequest import request
from help import help_main
from keywords import (horny_recog_phrases, joker_recog_phrases, monkey_emotes,
                      monkey_recog_phrases, yo_recog_phrases)
from todo import todo_add, todo_main, todo_p, todo_rm, todo_view

"""
Load all variables (Bot guild and bot token))
"""
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
todo_list = []

bot = commands.Bot(command_prefix='~', help_command=None) #Establish a command prefix to trigger the bot

@bot.command(pass_context = True)
async def help(ctx, *help_args):
    """
    Standard canned help message. Contents are stored in a text file 'help.txt', monke.txt, horny.txt, joker.txt, and todo.txt
    The various methods and functions were split into multiple help files so when one needs help they don't have to see one large list
    """
    resp = help_main(help_args)
    await ctx.channel.send(resp) #After file has been read and formatted, send as one message to the channel the command was called from

@bot.command(pass_context = True)
async def bugfact(ctx, *bf):
    if len(bf) > 0:
        await ctx.channel.send(file = discord.File("media/bugfacts/"+bf[0]+".jpg"))
    else:
        await ctx.channel.send(file = discord.File("media/bugfacts/"+str(r.randrange(1,67))+".jpg"))

@bot.command(pass_context = True)
async def clear(ctx):
    """
    Clear code-monkey screen
    """
    channel = bot.get_channel(802923855161065495)
    if ctx.message.author.id == 249542964844429313:
        await channel.send("⠀\n"*42)
    else:
        await ctx.channel.send("no")
        
@bot.command(pass_context = True)
async def status(ctx):
    await ctx.channel.send("Manually updating status")
    change_daily_status()

@bot.command(pass_context = True)
async def miner(ctx, *miner_args):

    if miner_args[0] == "config":
        with open("miners/"+str(ctx.message.author.id)+".txt", "w+") as fp:
            fp.write(str(miner_args[1]).strip())
        await ctx.channel.send("Miner configured")
    if miner_args[0] == "view":
        miner_ID = "";
        with open("miners/"+str(ctx.message.author.id)+".txt", "r") as fp:
            miner_ID = fp.readline()
        resp = request(str(miner_ID),"a")
        await ctx.channel.send(resp)

@bot.command(pass_context = True)
async def todo(ctx, *todo_arg):
    """
    This handles todos that typically have to do with the bot.
    """
    todo_arg = list(todo_arg)
    todo_arg[0] = str(todo_arg[0]).lower()

    resp = todo_main(todo_arg, todo_arg[0], str(ctx.message.author.id))

    await ctx.channel.send(resp)

@bot.event
async def on_ready():
    """
    When bot is being established, run through this (send message to signify bot has started)
    """   
    guild = None 
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        f"Today's Date is: "+dt.date.today().strftime('%d-%m-%Y')
    )
    channel = bot.get_channel(802923855161065495)
    await channel.send("**Bot Established**")
    change_daily_status.start()
    #COMMENT BELOW OUT IF YOU DONT NEED THE DAILY TASK
    daily_task.start()

@tasks.loop(hours=24)
async def change_daily_status():
    """
    Updates the bot's status via "Playing game: , based on the day of the week"
    """
    while True:
        channel = bot.get_channel(426547798704521216) #ID of #aids channel in my server
        day_status = ["More like monGAY","wait it fucking tueaday .", ":dizzy: Wooback Wednesday","dababy dursday","Gotta get down on friday","FREEDOM!","Fuk. Class tomorrow"] #Status for each dotw
        dotw = dt.datetime.today().weekday() #Day of the week
        await bot.change_presence(activity=discord.Game(name=day_status[dotw]))
        await bot.get_channel(802923855161065495).send("Daily status updated")
        if dotw == 3:
            await channel.send(file=discord.File('media/dababy.gif'))
        
        count = 0
        while True:
            if count <= 2:
                count += 1
                await asyncio.sleep(60*60) #Sleep for an hour (but 3 times) -> Update every 3 hours
            else:
                break

@tasks.loop(hours=24)
async def daily_task():
    """
    This checks for the completed daily health screen and informs @me via discord ping if it has been completed successfully or not
    """
    while True:
        channel = bot.get_channel(802923855161065495)
        screen = dt.date.today().strftime('%d-%m-%Y')+".png"
        if(os.path.exists("../dailyHealthBot/screens/"+screen)):
            await channel.send("*Found Daily Health Screen result* "+"<@249542964844429313>")
        else:
            await channel.send("*unable to locate today's completed daily health screen* "+"<@249542964844429313>")
        while dt.datetime.now().hour != 9:
            await asyncio.sleep(60*10) #If it's not 9am sleep for 10 minutes and check again

@bot.event
async def on_message(message):
    """
    Bot checks sent messages. If a keyword or command is found, execute
    """
    if message.author == bot.user: #If the bot sends a message, ignore it (therefore no recursion)
        return
    SPAM_COUNT = 0
    if "~" not in message.content: #Make sure that it's not a command where the keyword was found (this was an issue in the help calls)
        msg = str(message.content).lower().translate(str.maketrans('', '', string.punctuation)).split() #Get rid of punctuation and split message
        for keyword in msg:
            if not any(keyword in word and len(word) > len(keyword) for word in msg): #If keyword triggered, add reaction depending on msg
                if keyword in horny_recog_phrases:
                    await message.add_reaction("<:bonk:811325146316668958>")
                    SPAM_COUNT+=1
                    break
                elif keyword in joker_recog_phrases:
                    await message.add_reaction("<:FunnyMan:776139957768945704>")
                    SPAM_COUNT+=1
                    break
                elif keyword in monkey_recog_phrases:
                    response = r.choice(monkey_emotes)
                    await message.add_reaction(response)
                    SPAM_COUNT+=1
                    break
                elif keyword in yo_recog_phrases:
                    await message.add_reaction("🇾") #Regional y symbol
                    await message.add_reaction("<:OMEGALUL:658807091200393217>")
                    SPAM_COUNT+=1
                    break        
    await bot.process_commands(message)
bot.run(TOKEN)