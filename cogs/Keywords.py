import discord
import random as r
import string
from discord.ext import commands
import os
import json
from simplejson import JSONDecodeError


class Keywords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filePath = "jsonData.json"

    @commands.command(name='bugfact')
    async def bugfact(self, ctx, *bf):
        """Send a random bugfact [or the one designated] to channel it was called from

        Args:
            ctx (discord - context): Context of message that triggered command
            *bf (int): Optional bugfact number to be called
        """
        if len(bf) > 0:
            await ctx.channel.send(file=discord.File("media/bugfacts/"+bf[0]+".jpg"))
        else:
            await ctx.channel.send(file=discord.File("media/bugfacts/"+str(r.randrange(1, 67))+".jpg"))

    @commands.Cog.listener()
    async def on_message(self, message):
        """Bot checks sent messages. If a keyword or command is found, execute

        Args:
            message (str): Keyword / command recognized
        """
        if message.author == self.bot.user:  # If the bot sends a message, ignore it (therefore no recursion)
            return

        if os.path.exists(self.filePath):
            with open(self.filePath, 'r') as fp:
                try:
                    # Load JSON Object
                    JSONData = json.load(fp)['keywords']
                except ValueError as e:
                    print(e, "Value Error")

        monkey_recog_phrases = JSONData['monkey_recog_phrases']
        monkey_emotes = JSONData['monkey_emotes']
        horny_recog_phrases = JSONData['horny_recog_phrases']
        joker_recog_phrases = JSONData['joker_recog_phrases']
        yo_recog_phrases = JSONData['yo_recog']

        # Make sure that it's not a command where the keyword was found (this was an issue in the help calls)
        if "~" not in message.content:
            msg = str(message.content).lower().translate(str.maketrans(
                '', '', string.punctuation)).split()  # Get rid of punctuation and split message\
            for keyword in msg:
                # If keyword triggered, add reaction depending on msg
                if not any(keyword in word and len(word) > len(keyword) for word in msg):
                    if keyword in monkey_recog_phrases:
                        response = r.choice(monkey_emotes)
                        await message.add_reaction(response)
                        break
                    elif keyword in horny_recog_phrases:
                        await message.add_reaction("<:bonk:811325146316668958>")
                        break
                    elif keyword in joker_recog_phrases:
                        await message.add_reaction("<:FunnyMan:776139957768945704>")
                        break
                    elif keyword in yo_recog_phrases or "@yo" in message.content or "yo?" in message.content:
                        await message.add_reaction("🇾")  # Regional y symbol
                        await message.add_reaction("<:OMEGALUL:658807091200393217>")
                        break
            await asyncio.sleep(2)


def setup(bot):
    bot.add_cog(Keywords(bot))
