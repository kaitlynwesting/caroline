import discord
from discord.ext import commands
from discord.utils import get

# A simple filter bypassing checker, which checks if violators have bypassing roles

async def bypass_check(message):
    
    if message.guild is not None: # Do not want bot to check DMs
        if message.author.bot == False: # Do not want bot to check webhooks or other bots
            mod = get(message.guild.roles, name = "Moderator")
            admin = get(message.guild.roles, name = "Admin")
            owner = get(message.guild.roles, name = "Owner")

            omitted_roles = [mod, admin, owner]

            # If author has any of the above roles, they are exempt from the filter
            return any(True for role in message.author.roles if role in omitted_roles)
