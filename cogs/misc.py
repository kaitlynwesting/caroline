import discord
import traceback
import sys
import random
from discord.ext import commands
from discord.utils import get

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! The latency is {round(self.bot.latency, 2)} milliseconds.")
        

def setup(bot):
    bot.add_cog(Misc(bot))