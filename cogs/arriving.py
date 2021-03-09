import asyncio

import discord
from discord.ext import commands
from discord.utils import get

import sys
import traceback

# COG FOR NEW ARRIVALS AND DEPARTS

class Rules(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot 
        
    # JOIN LOGGER
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="logs")
        await channel.send(f"{member.mention} has joined us.")

    # LEAVE LOGGER
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="logs")
        await channel.send(f"{member.mention} has left.")
    
# binds the cog to the client file
def setup(bot):
    bot.add_cog(Rules(bot)) 



