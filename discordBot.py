#!/usr/bin/python3
# bot.py

#Standard packages
import asyncio
import datetime as dt
from logging import disable
import os
import random as r
import string

#Custom packages
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from minersRequest import request,get_spaces
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
OWNER_ID = os.getenv('OWNER_ID')
MINER_ID = os.getenv('MY_ID')
todo_list = []

bot = commands.Bot(command_prefix='~', help_command=None) #Establish a command prefix to trigger the bot

CODE_MONKE = 802923855161065495
SPACER = "`| "+ "-"*len(MINER_ID) +" |`\n"

@bot.command(pass_context = True)
async def help(ctx, *help_args):
    """Standard canned help message. Contents are stored in a text file 'help.txt', monke.txt, horny.txt, joker.txt, and todo.txt
    The various methods and functions were split into multiple help files so when one needs help they don't have to see one large list

    Args:
        ctx (discord - context): Context of message that triggered command
    """
    resp = help_main(help_args)
    await ctx.channel.send(resp) #After file has been read and formatted, send as one message to the channel the command was called from

@bot.command(pass_context = True)
async def bugfact(ctx, *bf):
    """Send a random bugfact [or the one designated] to channel it was called from

    Args:
        ctx (discord - context): Context of message that triggered command
        *bf (int): Optional bugfact number to be called 
    """
    if len(bf) > 0:
        await ctx.channel.send(file = discord.File("media/bugfacts/"+bf[0]+".jpg"))
    else:
        await ctx.channel.send(file = discord.File("media/bugfacts/"+str(r.randrange(1,67))+".jpg"))
        
@bot.command()
async def check(ctx):
    """Manually check if daily health screen has been completed

    Args:
        ctx (discord - context): Context of message that triggered command
    """
    channel = bot.get_channel(CODE_MONKE)
    screen = dt.date.today().strftime('%d-%m-%Y')+".png"
    if(os.path.exists("../dailyHealthBot/screens/"+screen)):
        await channel.send("*Found Daily Health Screen result* "+"<@249542964844429313>")
    else:
        await channel.send("*unable to locate today's completed daily health screen* "+"<@249542964844429313>")

@bot.command(pass_context = True)
async def clear(ctx):
    """Clear code-monkey screen

    Args:
        ctx (discord - context): Context of message that triggered command
    """
    channel = bot.get_channel(CODE_MONKE)
    if ctx.message.author.id == OWNER_ID:
        await channel.send("⠀\n"*42)
    else:
        await ctx.channel.send("You aren't allowed to clear messages")
        
@bot.command(pass_context = True)
async def miner(ctx, *miner_args):
    """Overall function associated with my current eth miner that can also be configured for other users.add()
    Currently using 2miners API, and as such the actual site it is pulling from is eth.2miners.com

    Args:
        ctx (discord - context): Context of message that triggered command
    """
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
async def note(ctx,*args):
    """Send a DM to the user (acts as a reminder)

    Args:
        ctx (discord - context): Context of message that triggered command
        *args (string): The message
    """
    note_resp = "".join([i+" " for i in args])
    await ctx.author.send(note_resp)
    await ctx.channel.send("Note DM'd to you <@{id}>".format(id=ctx.author.id))
          
@bot.command(pass_context = True)
async def status(ctx):
    """Manually update daily status

    Args:
        ctx (discord - context): Context of message that triggered command
    """
    await ctx.channel.send("Manually updating status")
    change_daily_status()

@bot.command(pass_context = True)
async def todo(ctx, *todo_arg):
    """Generate TODOs for individual users in a persistent method

    Args:
        ctx (discord - context): Context of message that triggered command
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
    channel = bot.get_channel(CODE_MONKE)
    await channel.send("**Bot Established**")
    change_daily_status.start()
    check_workers.start()
    #COMMENT BELOW OUT IF YOU DONT NEED THE DAILY TASK
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

@tasks.loop(hours=2)
async def check_workers():
    channel = bot.get_channel(CODE_MONKE)
    while True:
        workers = request(str(MINER_ID),"w")
        if not workers  == []:
            offline_workers = [i for i in workers if i[1] == 'True']
            if not offline_workers == []:
                resp = SPACER
                resp += "".join(["`| "+MINER_ID+get_spaces(MINER_ID,MINER_ID)+" |`\n"+SPACER])
                resp += "`| Workers Offline: " + get_spaces(MINER_ID,"Workers Offline: ")+"|`\n"+"".join(["`|      "+i+get_spaces(MINER_ID,"     "+i)+" |`\n"+SPACER for i in offline_workers])
                resp += SPACER
                await channel.send(resp+"<@{owner}>".format(owner = OWNER_ID))
        else:
            await channel.send("Workers offline <@{owner}>".format(owner=OWNER_ID))
        await asyncio.sleep(60*60*2) #Sleep for 2 hours
        
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
            
async def get_diff(message,MAX_HIST):
    """WIP Function for implementing a SPAM checker for the discord bot

    Args:
        message (string): The message sent
        MAX_HIST (int): Max number of messages to pull from channel for historical context

    Returns:
        int: abs val of the second difference between users last message and current message
    """
    msg_hist = await message.channel.history(limit=MAX_HIST+1).flatten() #Fetch last MAX_HIST messages from channel
    user_in_last_msgs = [bool(message.author.id == i.author.id) for i in msg_hist][1:] #Exclude most recent message
    print("user in last messages: "+ str(user_in_last_msgs))
    if True in user_in_last_msgs:
        user_msg_diff = (message.created_at - msg_hist[user_in_last_msgs.index(True)].created_at).total_seconds()
        # print("Curr Msg created at:",message.created_at)
        # print("msg_hist created at:", msg_hist[user_in_last_msgs.index(True)].created_at)
        print("new user diff " + str(user_msg_diff) + " based on message "+message.content)
    else:
        user_msg_diff = 100 #Init as allowing message  
    return abs(user_msg_diff)

@bot.event
async def on_message(message):
    """Bot checks sent messages. If a keyword or command is found, execute

    Args:
        message (str): Keyword / command recognized
    """
    if message.author == bot.user: #If the bot sends a message, ignore it (therefore no recursion)
        return
    
    TIMEOUT = 2 #Number of seconds to timeout bot per user
    MAX_HIST = 5 #Pull last 5 messages sent to channel. Probably should be higher if a more active channel
    
    user_diff = await get_diff(message, MAX_HIST)
    
    if "~" not in message.content: #Make sure that it's not a command where the keyword was found (this was an issue in the help calls)
        msg = str(message.content).lower().translate(str.maketrans('', '', string.punctuation)).split() #Get rid of punctuation and split message
        for keyword in msg:
            if not any(keyword in word and len(word) > len(keyword) for word in msg): #If keyword triggered, add reaction depending on msg
                if keyword in horny_recog_phrases:
                    await message.add_reaction("<:bonk:811325146316668958>")
                    break
                elif keyword in joker_recog_phrases:
                    await message.add_reaction("<:FunnyMan:776139957768945704>")
                    break
                elif keyword in monkey_recog_phrases:
                    response = r.choice(monkey_emotes)
                    await message.add_reaction(response)
                    break
                elif keyword in yo_recog_phrases:
                    await message.add_reaction("🇾") #Regional y symbol
                    await message.add_reaction("<:OMEGALUL:658807091200393217>")
                    break
    await bot.process_commands(message)
    
bot.run(TOKEN)