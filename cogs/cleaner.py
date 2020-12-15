import discord
import traceback
import sys
import random
import datetime
from discord.ext import commands

class Cleaner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def clean(self, ctx, amount=2, before=):
        await ctx.channel.purge(limit=amount + 1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True)
        

    

def setup(bot):
    bot.add_cog(Cleaner(bot))