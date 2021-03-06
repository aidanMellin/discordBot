from discord.ext import commands
import discord
from sys import version_info as sysv
from os import listdir
import string
import asyncio

class Dev(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	#This is the decorator for events (inside of cogs).
	async def on_ready(self):
		print(f'Python {sysv.major}.{sysv.minor}.{sysv.micro} - Disord.py {discord.__version__}\n')
		#Prints on the shell the version of Python and Discord.py installed in our computer.
		await self.bot.get_channel(802923855161065495).send(f'Python {sysv.major}.{sysv.minor}.{sysv.micro} - Disord.py {discord.__version__}')

	@commands.command(name='reloadall', hidden=True)#This command is hidden from the help menu.
	@commands.is_owner()
	async def reload_all(self, ctx):
		"""This commands reloads all the cogs in the `./cogs` folder.

		Note:
			This command can be used only from the bot owner.
			This command is hidden from the help menu.
			This command deletes its messages after 20 seconds."""

		message = await ctx.send('Reloading...')
		await ctx.message.delete()
		try:
			for cog in listdir('./cogs'):
				if cog.endswith('.py') == True:
					self.bot.reload_extension(f'cogs.{cog[:-3]}')
		except Exception as exc:
			await message.edit(content=f'An error has occurred: {exc}', delete_after=20)
		else:
			await message.edit(content='All cogs have been reloaded.', delete_after=20)

	@commands.command(name='clear', hidden=True)
	@commands.is_owner()
	async def clear(self,ctx):
		#TODO clear function \n * 42
		pass

	@commands.command(name='gag')
	async def gag(self, ctx):
		#TODO Gag function
		pass

	@commands.command(name='python')
	async def python(self,ctx):
		resp = "```Python\n{code}```".format(code = str(ctx.message.content).replace("~python",""))
		await ctx.message.delete()
		await ctx.channel.send(resp)
		
def setup(bot):
	bot.add_cog(Dev(bot))
