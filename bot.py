import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import os
import settings
import datetime

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = discord.ext.commands.Bot(command_prefix = settings.prefix, intents = intents)
print("Loading discord.py version", discord.__version__, ", starting...")

# bot loading messages on ready
@client.event
async def on_ready():
    print("I am ready!")

    # set the now playing status
    if settings.nowplaying:
            print("Setting now playing game...", flush= True)
            await client.change_presence(activity=discord.Game(name=settings.nowplaying))
            print("-----")

    # loader for cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try: 
                client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Failed to load {filename}")
    print("-----")

    # vanity print messages
    print("Logged in as:", client.user.name)
    print("My id is:", client.user.id)
    print("My prefix is:", settings.prefix)
    print('-----')
    # heroku ps -a robolydia #(twd) tie city 206

client.run(settings.token)