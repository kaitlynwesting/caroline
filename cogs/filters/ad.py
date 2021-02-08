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

# COG TO FILTER CHAT FOR ADVERTISEMENTS
class Ad(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ANTI-ADVERTISING FILTER
    @commands.Cog.listener()
    async def on_message(self, message):

        punishment_time = 10

        with open('cogs/texts/infraction.txt', 'r') as f:
            rules = f.readlines()

        rule1 = (rules[10])[0:-1]
        rule2 = (rules[11])[0:-1]
        rule3 = ((rules[14])[0:-1]).replace("punishment", str(punishment_time))
        
        infraction_description = f"__Violation of {rule1}: {rule2}__ \n{rule3}. {rules[13]} "

        # Detect advertisements only in the server!
        if message.guild is not None:
            # Split each message to fragments.
            splitted = message.content.split()

            # Examine each message for discord.gg links and disboard links, and concat into a list of invites in the message.
            discord_invites = [s for s in splitted if "discord.gg" in s]
            disboard_invites = [s for s in splitted if "disboard.org" in s]
            invites = discord_invites + disboard_invites

            # Replace useless https:// prefix for matching.
            invites = [i.replace("https://", "") for i in invites]

            # Fetch list of all active invites and our disboard page, and concat into a list of server invites.
            server_invite_raw = await message.guild.invites()
            server_invite_codes = [i.url for i in server_invite_raw]
            server_invite_codes = [i.replace("https://", "") for i in server_invite_codes]
            server_disboard_invite = ["disboard.org/server/join/777207888846389270", "disboard.org/servers/tag/photoshop", "disboard.org"]
            server_invites = server_invite_codes + server_disboard_invite
            
            # If invite(s) have been detected in the user's message...
            if len(invites) > 0:
                is_advertising = not all(i in server_invites for i in invites)
                print(is_advertising)
                if is_advertising is True:
                    # Delete the advertisement.
                    await message.channel.purge(limit=1)

                    await infraction.infraction_notification(message, "advertising", punishment_time)
                    await infraction.infraction_auto_embed(message, "advertising", infraction_description)
                    await infraction.infraction_tempmute(message, punishment_time)

def setup(bot):
    bot.add_cog(Ad(bot))