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
    @commands.has_permissions(kick_members = True)
    async def clean(self, ctx, amount=2):

        await ctx.channel.purge(limit=amount + 1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True)


    """ @commands.command()
    @commands.has_permissions(kick_members = True)
    async def wipe(self, ctx, amount=2, before=datetime.datetime.now(), after = datetime.datetime(2020, 5, 17)):
        await ctx.channel.purge(limit=amount + 1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True) """
        

    

def setup(bot):
    bot.add_cog(Cleaner(bot))