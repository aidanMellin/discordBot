#!/usr/bin/python3
# bot.py
import os
from os import path

import discord
from discord.file import File
from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv

import random
from datetime import date
import datetime as dt
import asyncio
import time

"""Load all variables (Bot guild and bot token))
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
    help_args = list(help_args)
    resp = ''
    if len(help_args) < 1: #No arg with help call
        resp = "Usage:\n**~help [monke/joker/horny/todo]**"
    else: #Help call containing arg
        call = help_args[0]
        if "monke" in call: #Open monke.txt
            with open('help/monke.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "joker" in call: #Open joker.txt
            with open('help/joker.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "horny" in call: #Open horny.txt
            with open('help/horny.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "todo" in call: #Open todo.txt
            with open('help/todo.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        else:
            resp = "invalid call"
    await ctx.channel.send(resp) #After file has been read and formatted, send as one message to the channel the command was called from

def todo_add(author, todo_arg):
    with open(+author+".txt", 'a+') as fp: #Open as a+ so it appends to the bottom of the file (or creates it)
        fp.seek(0) #Redundancy
        todo_add = " ".join(todo_arg[1:]) #Each call will have one todo to add, so combine the split args into one string to add to todo
        fp.write(todo_add)
        fp.write("\n")

def todo_rm(author, todo_arg):
     with open(author+".txt", 'r') as fp: #Read the lines and store to a list for easier manipulation
        lines = fp.readlines()
        if len(todo_arg) > 2: #Multiple rm calls
            rm_obj = todo_arg[1:]
            rm_obj = [int(i) for i in rm_obj] #Int all of the numbers in the list
            rm_obj.sort(reverse=True) #Sort in descending order to account for list deletion when removing
            for i in range(len(rm_obj)):
                del lines[int(rm_obj[i])-1]
        else: #Only one remove call
            del lines[int(todo_arg[1])-1]
        with open(author+".txt", 'w+') as fp:
            for line in lines:
              fp.write(line) #Rewrite the remaining lines from the lines list

def todo_view(author):
    with open(author+".txt", 'r+') as fp:
        fp.seek(0) #Redundancy
        resp = ""
        line = fp.readline()
        if(line == ""): #Empty todo list
            resp = "Nothing currently in TODO List"                                                                    
        count = 1
        while line: #Put the entire todo list in one formatted string so that there is no lag when sending it to the discord chat
            resp += "".join(str(count)+". "+line)
            line = fp.readline()
            count += 1
    return resp

def todo_p(author, todo_arg):
    with open(author+".txt", 'r+') as fp:
        pos = fp.tell()
        line = fp.readlines()
        line_manip = line[int(todo_arg[1])-1]
        print(line_manip)
        if not "*" in line_manip:
            line_manip = "**"+line[int(todo_arg[1])-1].strip("\n")+"**\n"
        else:
            time.sleep(2)
            print("removing **")
            line_manip = line_manip.replace("*","")
            print("New Line manip = "+line_manip)
        line[int(todo_arg[1])-1] = line_manip
    with open(author+".txt","w") as fp:
        for i in range(len(line_manip)):
            fp.write(line[i])

@bot.command(pass_context = True)
async def todo(ctx, *todo_arg):
    """
    This handles todos that typically have to do with the bot. Need to make it persistent based on a text file that will be saved in its directory. Should also add that it should send todos when it sends the daily health check
    """
    todo_arg = list(todo_arg)
    todo_arg[0] = str(todo_arg[0]).lower()
    if todo_arg[0] == "test":
        todo_add("todo_persist/"+str(ctx.message.author.id),["","test1"])
        todo_add("todo_persist/"+str(ctx.message.author.id),["","test2"])
        todo_add("todo_persist/"+str(ctx.message.author.id),["","test3"])
        await ctx.channel.send("TODO Test Completed")
        resp = todo_view("todo_persist"+str(ctx.message.author.id))
        await ctx.channel.send(resp)

    elif todo_arg[0] == 'add': #Adding things to todo list
        todo_add("todo_persist/"+str(ctx.message.author.id),todo_arg)
        await ctx.channel.send("TODO added")

    elif 'remove' in todo_arg[0] or "rm" in todo_arg[0]: #Remove a (batch) of todo(s)
        todo_rm("todo_persist/"+str(ctx.message.author.id), todo_arg)
        await ctx.channel.send("TODO deleted")

    elif todo_arg[0] == "view": #Print a formatted version of the user-specific todo list
        resp = todo_view("todo_persist/"+str(ctx.message.author.id))
        await ctx.channel.send(resp)

    elif "p" in todo_arg[0][0]: #A prioritize method: Bolds the multiple? calls
        todo_p("todo_persist/"+str(ctx.message.author.id),todo_arg)
        await ctx.channel.send("TODO Prioritized")

    elif todo_arg[0] == "clear":
        open("todo_persist/"+str(ctx.message.author.id)+".txt", 'w').close()
        await ctx.channel.send("TODO Cleared")
    #await ctx.channel.send(todo_arg)

@bot.event
async def on_ready():
    """When bot is being established, run through this (send message to signify bot has started)
    """   
    guild = None 
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        f"Today's Date is: "+date.today().strftime('%d-%m-%Y')
    )
    channel = bot.get_channel(802923855161065495)
    await channel.send("**Bot Established**")
    change_daily_status.start()
    #COMMENT BELOW OUT IF YOU DONT NEED THE DAILY TASK
    daily_task.start()

@tasks.loop(hours=24)
async def change_daily_status():
    channel = bot.get_channel(426547798704521216) #ID of #aids channel in my server
    day_status = ["","","wait it fucking tueaday .", "<:dizzy:1b3817ca3b1dc991baefdb3079ed0624>Wooback Wednesday","dababy dursday","",""] #Status for each dotw
    dotw = dt.datetime.today().weekday() #Day of the week
    await bot.change_presence(activity=discord.Game(name=day_status[dotw]))
    if dotw == 4:
        await channel.send(file=discord.File('media/dababy.gif'))

@change_daily_status.before_loop
async def before_status():
    for _ in range(60*60*24):
        if dt.datetime.now().hour == 17:
            print("updating status")
            return
        await asyncio.sleep(60*30) #Check every 30 minutes

@tasks.loop(hours=24)
async def daily_task():
    """
    This checks for the completed daily health screen and informs @me via discord ping if it has been completed successfully or not
    """
    channel = bot.get_channel(802923855161065495)
    screen = date.today().strftime('%d-%m-%Y')+".png"
    if(os.path.exists("../dailyHealthBot/screens/"+screen)):
        await channel.send("*Found Daily Health Screen result* "+"<@249542964844429313>")
    else:
        await channel.send("*unable to locate today's completed daily health screen* "+"<@249542964844429313>")
    
@daily_task.before_loop
async def before_task():
    """
    Actually accounts for the 24 hour wait before loop
    """
    for _ in range(60*60*24):  # loop the hole day
        if dt.datetime.now().hour == 9:  # 24 hour format
            print("Checking Daily Health Result")
            return
        await asyncio.sleep(60*10)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    monkey_recog_phrases = [
        ":monkey:",
        ":gorilla:",
        ":orangutan:",
        ":monkey_face:",
        "monke",
        "monkey",
        "pimp",
        "pimps",
        "chimp",
        "chimpin",
        "chimps",
        "train",
        "orangutan",
        "orangutans"
        "gorilla",
        "gorillas",
        "banana",
        "bananas",
        "peanut",
        "peanuts",
        "primate",
        "primates",
        "ape",
        "apes",
        "mongoloid",
        "mongoloids"
    ]

    monkey_emotes = [
        ":monkey:",
        ":gorilla:",
        ":orangutan:",
        ":monkey_face:",
        "<:squadW:645483642381926421>"
    ]

    joker_recog_phrases = [
        "society",
        "societies",
        "racist",
        "racists",
        "racism",
        "funny",
        "prejudice",
        "terrorist",
        "terrorists",
        "terrorism",
        "abuse",
        "abuser",
        "abusers",
        "kino",
        "kinophile",
        "kinophiles",
        "a24",
        "misogyny",
        "phile",
        "philes",
        "pedo",
        "pedos",
        "pedophile",
        "pedophiles"
    ]

    horny_recog_phrases = [
        "horny",
        "gasm",
        "hot",
        "sexy",
        "cute",
        "butt",
        "feet",
        "toes",
        "tits",
        "boobs",
        "<:triumph:805133291703369739>",
        "cum"
    ]

    if "~" not in message.content:
        for i in range(len(horny_recog_phrases)):
            if horny_recog_phrases[i] in str(message.content).lower():
                keyword = horny_recog_phrases[i]
                if not any(keyword in word and len(word) > len(keyword) for word in message.content.split()):
                    await message.channel.send(file = discord.File('horny.png'))
                    break

        for i in range(len(joker_recog_phrases)):
            if joker_recog_phrases[i] in str(message.content).lower():
                keyword = joker_recog_phrases[i]
                if not any(keyword in word and len(word) > len(keyword) for word in message.content.split()):
                    await message.channel.send("<:FunnyMan:776139957768945704>")
                    break

        for i in range(len(monkey_recog_phrases)): #Check if message has keywords
            if monkey_recog_phrases[i] in str(message.content).lower():
                keyword = monkey_recog_phrases[i]
                if not any(keyword in word and len(word) > len(keyword) for word in message.content.split()):
                    response = random.choice(monkey_emotes)
                    await message.channel.send(response)
                    break
    
    await bot.process_commands(message)

bot.run(TOKEN)
