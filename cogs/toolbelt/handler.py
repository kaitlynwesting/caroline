import discord
from discord.ext import commands
from discord.utils import get
import sys
import traceback


class Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """

        :param ctx: commands.Context
        :param error: commands.CommandError
        :return:
        """

        if getattr(ctx, 'error_handled', False):  # or just hasattr
            return

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"Missing required argument(s): {error.param}"
            )

            print(ctx.command.short_doc)  # YES
            # await ctx.send_help(ctx.command)

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to run this command.", file=discord.File("./media/image1.jpg"))

        # CAN'T FIND COMMAND
        elif isinstance(error, commands.CommandNotFound):

            if ctx.message.content.startswith("!d"):
                return

            await ctx.send("Couldn't find that command, sorry.")

        elif isinstance(error, TypeError):
            await ctx.send(f"TypeError. Oof. {error}")

        else:
            print(error)
            await ctx.send(str(error)[:1000])
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)


def setup(bot):
    bot.add_cog(Handler(bot))
