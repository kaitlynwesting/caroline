import asyncio
from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands
from discord.utils import get

from ..utils import infraction
import os
import pytz
import random
import requests
import sys
import string
import time
import traceback

# COG TO FILTER CHAT FOR MASS MENTIONS
class Mass(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ANTI-ADVERTISING FILTER
    @commands.Cog.listener()
    async def on_message(self, message):
        # Detect advertisements only in the server!
        if message.guild is not None:
            mod = get(message.guild.roles, name = "Moderator")
            admin = get(message.guild.roles, name = "Admin")

            omitted_roles = [mod, admin]

            punishment_time = 10

            with open('cogs/texts/infraction.txt', 'r') as f:
                rules = f.readlines()

            rule1 = (rules[2])[0:-1]
            rule2 = (rules[3])[0:-1]
            rule3 = ((rules[14])[0:-1]).replace("punishment", str(punishment_time))
            
            infraction_description = f"""__Violation of {rule1}: {rule2}__ 
            Apparently, you deemed yourself important enough to disturb others.
            {rule3}. {rules[13]} """
            
            # The action parts.
            if not any(r in message.author.roles for r in omitted_roles):
                if "@everyone" in message.content or "@here" in message.content:
                    await infraction.infraction_notification(message, "mass mentions", punishment_time)
                    await infraction.infraction_auto_embed(message, "mass mentions", infraction_description)
                    await infraction.infraction_tempmute(message, punishment_time)

def setup(bot):
    bot.add_cog(Mass(bot))