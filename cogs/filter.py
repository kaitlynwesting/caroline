import discord
import traceback
import sys
import random
from discord.ext import commands
from discord.utils import get

class Filter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # NO ADVERTISING
    @commands.Cog.listener()
    async def on_message(self, message):
        mod = get(message.guild.roles, name="Moderator")

        if "discord.gg" in str(message.content):
        
            if mod in message.author.roles:
                pass
            elif message.author.id == 785298572047417374: # Lydia id lol
                pass
            else:
                await message.channel.purge(limit=1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True)

        
        
    
        

def setup(bot):
    bot.add_cog(Filter(bot))