import discord
from discord.ext import commands
import os
import settings

description = """
Hello! I'm a bot written by Kaitlyn to provide some nice utilities.
"""

initial_extensions = (
    'cogs.meta',
    'cogs.splatoon',
    'cogs.rng',
    'cogs.mod',
    'cogs.profile',
    'cogs.tags',
    'cogs.lounge',
    'cogs.carbonitex',
    'cogs.api',
    'cogs.stars',
    'cogs.admin',
    'cogs.buttons',
    'cogs.reminder',
    'cogs.stats',
    'cogs.emoji',
    'cogs.config',
    'cogs.dpy',
    'cogs.funhouse',
)

print("Running discord.py version", discord.__version__, ", starting...")
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix=settings.prefix, intents=intents)  # help_command=help.MyHelp()

@bot.event
async def on_ready():
    print("Finished initialising bot, setting status...", flush=True)

    await bot.change_presence(
        activity=discord.Activity(status=discord.Status.idle,
                                  type=discord.ActivityType.listening,
                                  name=settings.nowplaying)
    )

    print("-----")

    for folder in (os.listdir('./cogs')):
        print(folder)
        for file in os.listdir(f'./cogs/{folder}'):
            if file.endswith(".py"):
                if not file.startswith("__init__"):
                    loading_path = f"cogs.{folder}.{file[:-3]}"
                    try:
                        bot.load_extension(loading_path)
                    except Exception as e:
                        print(f"Could not load {file} due to {e}")


@bot.command(dm_only=True)
async def test(ctx):
    print(1)


# heroku ps -a robolydia #(twd) tie city 206

bot.run(settings.token)
