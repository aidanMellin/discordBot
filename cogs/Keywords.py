import discord
import random as r
import string
from discord.ext import commands

from keywords import (horny_recog_phrases, joker_recog_phrases, monkey_emotes, monkey_recog_phrases, yo_recog_phrases)

class Keywords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self,message):
        """Bot checks sent messages. If a keyword or command is found, execute
    
        Args:
            message (str): Keyword / command recognized
        """
        if message.author == self.bot.user: #If the bot sends a message, ignore it (therefore no recursion)
            return
        # TIMEOUT = 2 #Number of seconds to timeout bot per user
        # MAX_HIST = 5 #Pull last 5 messages sent to channel. Probably should be higher if a more active channel
    
        #user_diff = await get_diff(message, MAX_HIST)
    
        if "~" not in message.content: #Make sure that it's not a command where the keyword was found (this was an issue in the help calls)
            msg = str(message.content).lower().translate(str.maketrans('', '', string.punctuation)).split() #Get rid of punctuation and split message
            for keyword in msg:
                if not any(keyword in word and len(word) > len(keyword) for word in msg): #If keyword triggered, add reaction depending on msg
                    #await bot.get_channel(CODE_MONKE).send(keyword)
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
                        await message.add_reaction("🇾") #Regional y symbol
                        await message.add_reaction("<:OMEGALUL:658807091200393217>")
                        break
                        
def setup(bot):
	bot.add_cog(Keywords(bot))