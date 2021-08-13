import discord
import sys
import traceback

from discord.ext import commands



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

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        # if isinstance(error, commands.MissingRequiredArgument):
        #
        #     await ctx.send(
        #         f"Missing required argument(s): {error.param}"
        #     )
        #
        #     # print(ctx.command.short_doc)  # YES
        #     await ctx.send_help(ctx.command)

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to run this command.", file=discord.File("./media/image1.jpg"))

        elif isinstance(error, commands.CommandNotFound):

            if ctx.message.content.startswith("!d"):
                return

            return

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            traceback_message = traceback.format_exc()
            await ctx.send(traceback_message)
            await ctx.send(str(error)[:1000])


def setup(bot):
    bot.add_cog(Handler(bot))
