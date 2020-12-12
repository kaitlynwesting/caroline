import discord
from discord.ext import commands
import os

import settings

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = discord.ext.commands.Bot(command_prefix = settings.prefix, intents = intents)
# channel = client.get_channel(int(690290724994023519))
print("Loading discord.py version", discord.__version__, ", starting...")

@client.command() # this is a listener that listens for messages
async def wake(ctx, member:discord.Member):
    for channel in member.guild.channels:
        if str(channel) == "logs": # channel check here
            await channel.send(f"Test.") 

# if member:discord.Member is not a parameter, you must manually obtain the channel id.
# otherwise you can use member.guilds.channel to look for a matching channel string

@client.event
async def on_ready():
    print("I am ready!")

client.run(settings.token)