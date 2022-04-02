import sys
import traceback
from discord.ext import commands


class Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if getattr(ctx, 'error_handled', False):  # or just hasattr
            return

        # Safely unwrap the error
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, commands.CommandNotFound):
            return

        else:
            await ctx.send(f"```py\n{type(error).__name__}: {error}```",)

            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


async def setup(bot):
    await bot.add_cog(Handler(bot))
