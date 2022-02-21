import aiosqlite
import discord
import traceback
from discord.ext import commands
import settings
from cogs.dropdowns import DropdownView
from cogs.help import MyHelp

initial_extensions = (
    "cogs.events",
    "cogs.misc",
    "cogs.moderation",
    "cogs.rtd",
    "cogs.starboard",
    "cogs.toolkit",
    "cogs.handler",
)

testing_extensions = ("cogs.dropdowns",)

intents = discord.Intents(
    messages=True, guilds=True, reactions=True, members=True, presences=True
)

# bot = commands.Bot(
#     command_prefix=commands.when_mentioned_or(settings.prefix),
#     intents=intents
# )

print(f"discord.py, version {discord.__version__}")


# @bot.event
# async def on_connect():
#     bot.db = await aiosqlite.connect('data/guild.db')
#     bot.season_number = int((await(
#         await bot.db.execute("""SELECT value FROM config
#                                 WHERE name = (?)""", ('season_number',))).fetchone())[0])


# @bot.event
# async def on_ready():
#     print(f"Logged in. \n"
#           f"Name: {bot.user.name} \n"
#           f"Guilds: {str(len(bot.guilds))} \n"
#           f"-----")
#
#     await bot.change_presence(
#         activity=discord.Activity(
#             type=discord.ActivityType.listening,
#             name=settings.nowplaying)
#     )
#
#     for extension in testing_extensions:
#         try:
#             print(str(extension))
#             bot.load_extension(extension)
#         except Exception:
#             print(f"Failed to load extension '{extension}'\n"
#                   f"{traceback.format_exc()}")


class Caroline(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(settings.prefix),
            intents=intents,
            help_command=MyHelp(),
            activity=discord.Activity(type=discord.ActivityType.listening, name=settings.activity),
            status=discord.Status.idle
        )
        self.persistent_views_added = False

    async def on_connect(self):
        bot.db = await aiosqlite.connect("data/guild.db")
        bot.season_number = int(
            (
                await (
                    await bot.db.execute(
                        """SELECT value FROM config
                                    WHERE name = (?)""",
                        ("season_number",),
                    )
                ).fetchone()
            )[0]
        )

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(DropdownView())
            self.persistent_views_added = True

        print(
            f"Logged in. \n"
            f"Name: {bot.user.name} \n"
            f"Guilds: {str(len(bot.guilds))} \n"
            f"-----"
        )

        # await bot.change_presence(
        #     activity=discord.Activity(
        #     type=discord.ActivityType.listening,
        #     name="exactly 1 server"),
        #     status=discord.Status.dnd
        # )

        for extension in initial_extensions:
            try:
                print(str(extension))
                bot.load_extension(extension)
            except Exception:
                print(
                    f"Failed to load extension '{extension}'\n"
                    f"{traceback.format_exc()}"
                )


bot = Caroline()
bot.run(settings.token)
