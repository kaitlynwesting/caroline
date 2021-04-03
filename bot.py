import discord
from discord.ext import commands

import os

from discord.ext.commands import bot

import settings

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = discord.ext.commands.Bot(command_prefix=settings.prefix, intents=intents)  # help_command=None
print("Loading discord.py version", discord.__version__, ", starting...")


# bot loading messages on ready
@client.event
async def on_ready():

    print("I am ready!")

    # set the now playing status

    print("Setting now playing game...", flush=True)
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=settings.nowplaying))
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

        # try:
        #     print(os.listdir(f'./cogs/{item}'))
        # except NotADirectoryError as e:
        #     print("Oops, couldn't do that because of", e)

    print('over')
#     path = ["./cogs", "./cogs/filters"]
#     loading_path = ""
#     for folder in path:
#         for filename in os.listdir(folder):
#             if folder == "./cogs":
#                 loading_path = f"cogs.{filename[:-3]}"
#             elif folder == "./cogs/filters":
#                 loading_path = f"cogs.filters.{filename[:-3]}"
#
#             if filename.endswith(".py"):
#                 try:
#                     client.load_extension(loading_path)
#                     print(f"Loaded: {filename}")
#                 except Exception as e:
#                     print(e)
#                     print(f"Failed to load {filename}")
#         print("-----")
#
#     # vanity print messages
#     print("Logged in as:", client.user.name)
#     print("My id is:", client.user.id)
#     print("My prefix is:", settings.prefix)
#     print('-----')
#     # heroku ps -a robolydia #(twd) tie city 206
#
#
client.run(settings.token)
