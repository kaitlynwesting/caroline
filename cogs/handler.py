import discord
import sys
import traceback

from discord.ext import commands
from cogs.utils import constants
from cogs.utils.embed_template import error_embed


class Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """

        :param ctx:
        :param error: commands.CommandError
        :return:
        """

        if getattr(ctx, 'error_handled', False):  # or just hasattr
            return

        # Safely unwrap the error
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, commands.MissingRequiredArgument):

            await error_embed(ctx,
                              f"Oups! MissingRequiredArgument error with !{ctx.command}",
                              f"You are missing the below argument:",
                              f"```py\n{error.param}```",
                              f'{ctx.command.signature}',
                              constants.yellow)

            print(ctx.command.help)  # YES
            await ctx.send_help(ctx.command)

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to run this command.", file=discord.File("./media/image1.jpg"))

        elif isinstance(error, commands.CommandNotFound):

            if ctx.message.content.startswith("!d"):
                return

            return

        else:
            await error_embed(ctx,
                              f"Oups! Uncaught error with !{ctx.command}",
                              f"Severity: who knows?",
                              f"```py\n{type(error).__name__}: {error}```",
                              f'',
                              constants.yellow)
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



def setup(bot):
    bot.add_cog(Handler(bot))
