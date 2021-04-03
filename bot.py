import discord
from discord.ext import commands

import os
import settings

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = discord.ext.commands.Bot(command_prefix=settings.prefix, intents=intents)  # help_command=None
print("Loading discord.py version", discord.__version__, ", starting...")


# bot loading messages on ready
@client.event
async def on_ready():

    print("I am ready!")

    print("Setting now playing game...", flush=True)

    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=settings.nowplaying)
    )

    print("-----")

    # The below is a loader of cogs.
    # It browses every folder in the /cogs folder, and load files with .py extension.
    for folder in (os.listdir('./cogs')):
        for file in os.listdir(f'./cogs/{folder}'):
            if file.endswith(".py"):
                if not file.startswith("__init__"):
                    loading_path = f"cogs.{folder}.{file[:-3]}"
                    try:
                        client.load_extension(loading_path)
                    except Exception as e:
                        print(f"Could not load {file} due to {e}")

# heroku ps -a robolydia #(twd) tie city 206

client.run(settings.token)
