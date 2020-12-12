import discord
import traceback
import sys
import random
from discord.ext import commands

class Tip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    

def setup(bot):
    bot.add_cog(Tip(bot)) do not add yet