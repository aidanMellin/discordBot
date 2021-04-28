import discord
import datetime as dt
import os

from discord.ext import commands
from todo import todo_add, todo_main, todo_p, todo_rm, todo_view
from minersRequest import request,get_spaces

CODE_MONKE = 802923855161065495


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='check')
    async def check(self,ctx):
        """Manually check if daily health screen has been completed
    
        Args:
            ctx (discord - context): Context of message that triggered command
        """
        channel = self.bot.get_channel(CODE_MONKE)
        screen = dt.date.today().strftime('%d-%m-%Y')+".png"
        if(os.path.exists("../../dailyHealthBot/screens/"+screen)):
            await channel.send("*Found Daily Health Screen result* "+"<@249542964844429313>")
        else:
            await channel.send("*unable to locate today's completed daily health screen* "+"<@249542964844429313>")
    
    @commands.command(name='miner')
    async def miner(self,ctx, *miner_args):
        """Overall function associated with my current eth miner that can also be configured for other users.add()
        Currently using 2miners API, and as such the actual site it is pulling from is eth.2miners.com
    
        Usage:
            First run:
                **~miner config [ID]**
            
            Otherwise:
                **~miner [view]**
    
        Args:
            ctx (discord - context): Context of message that triggered command
            *miner_args - Either configuration information or command to view data
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
    
    @commands.command(name='note')
    async def note(self,ctx,*args):
        """Send a DM to the user (acts as a reminder)
    
        Usage:
            **~note [message to be DMd to you]**
    
        Args:
            ctx (discord - context): Context of message that triggered command
            *args (string): The message
        """
        note_resp = "".join([i+" " for i in args])
        await ctx.author.send(note_resp)
        await ctx.channel.send("Note DM'd to you <@{id}>".format(id=ctx.author.id))
    
    @commands.command(name='todo')
    async def todo(self,ctx, *todo_arg):
        """Generate TODOs for individual users in a persistent method
    
        Usage:
        	**~todo [add/remove/clear/view/p(rioritize)]** *secondary argument*
    
        Args:
            ctx (discord - context): Context of message that triggered command
        """
        todo_arg = list(todo_arg)
        todo_arg[0] = str(todo_arg[0]).lower()
    
        resp = todo_main(todo_arg, todo_arg[0], str(ctx.message.author.id))
    
        await ctx.channel.send(resp)

def setup(bot):
	bot.add_cog(Tools(bot))