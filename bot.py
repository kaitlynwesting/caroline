import aiosqlite
import discord
import traceback
from discord.ext import commands
import settings

# If you want to add more modules in the future

initial_extensions = (
    "cogs.arrivals",
    "cogs.badges",
    "cogs.events",
    "cogs.filters",
    "cogs.fun",
    "cogs.jail",
    "cogs.misc",
    "cogs.moderation",
    "cogs.rtd",
    "cogs.reddit",
    "cogs.starboard",
    "cogs.tags",
    "cogs.user",
    "cogs.toolkit",
    "cogs.handler",
)

testing_extensions = (
    "cogs.badges",
)

intents = discord.Intents(
    messages=True,
    guilds=True,
    reactions=True,
    members=True,
    presences=True
)

bot = commands.Bot(
    command_prefix=settings.prefix,
    intents=intents
)

print(f"discord.py, version {discord.__version__}")


@bot.event
async def on_connect():
    bot.db = await aiosqlite.connect('sql/guild.db')
    bot.season_number = int((await(
        await bot.db.execute("""SELECT value FROM config
                                WHERE name = (?)""", ('season_number',))).fetchone())[0])


@bot.event
async def on_ready():
    print(f"Logged in. \n"
          f"Name: {bot.user.name} \n"
          f"Guilds: {str(len(bot.guilds))} \n"
          f"-----")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=settings.nowplaying)
    )

    for extension in initial_extensions:
        try:
            print(str(extension))
            bot.load_extension(extension)
        except Exception:
            print(f"Failed to load extension '{extension}'\n"
                  f"{traceback.format_exc()}")


bot.run(settings.token)
