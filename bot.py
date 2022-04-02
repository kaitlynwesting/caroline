import aiosqlite
import discord
import traceback
from discord.ext import commands
import settings
from cogs.dropdowns import DropdownView
from cogs.help import MyHelp
from cogs.utils.views import Context

intents = discord.Intents(
    messages=True, message_content=True, guilds=True, reactions=True, members=True, presences=True
)


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
        self.initial_extensions = [
            "cogs.admin",
            "cogs.misc",
            "cogs.moderation",
            "cogs.photoshop",
            "cogs.meta",
            "cogs.handler",
        ]

    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    async def on_connect(self):
        bot.db = await aiosqlite.connect("data/guild.db")

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(DropdownView())
            self.persistent_views_added = True

        print(
            f"-----\n"
            f"Logged in using discord.py {discord.__version__}. \n"
            f"Name: {bot.user.name} \n"
            f"Guilds: {str(len(bot.guilds))} \n"
            f"-----"
        )

    async def setup_hook(self):
        print(f"Attempting to load {len(self.initial_extensions)} cogs...\n-----")

        for extension in self.initial_extensions:
            try:
                await bot.load_extension(extension)
                print(str(extension))
            except Exception:
                print(
                    f"Failed to load extension '{extension}'\n"
                    f"{traceback.format_exc()}"
                )


bot = Caroline()
bot.run(settings.token)
