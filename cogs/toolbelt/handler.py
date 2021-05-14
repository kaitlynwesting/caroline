import discord
from discord.ext import commands
from discord.utils import get
from utils import constants
import traceback


class Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Insufficient arguments.
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"Oops, {ctx.author.name}, looks like you missed the following arguments: \n"
                f"`{error.param}`"
            )

            print(ctx.command.short_doc)  # YES
            # await ctx.send_help(ctx.command)

        # INSUFFICIENT PERMISSIONS
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to run this command.", file=discord.File("./media/image1.jpg"))

        # CAN'T FIND COMMAND
        elif isinstance(error, commands.CommandNotFound):

            if not ctx.message.content.startswith("!d"):

                await ctx.send("Couldn't find that command, sorry.")

        # CAN'T FIND PERSON
        elif isinstance(error, commands.MemberNotFound):

            await ctx.send(
                "Couldn't find a member. If you don't know why that happened, see `!tag membernotfound`."
            )

        # ON COOLDOWN
        elif isinstance(error, commands.CommandOnCooldown):
            mod = get(ctx.guild.roles, name="Moderator")

            if mod in ctx.author.roles:
                try:
                    await ctx.reinvoke()
                except (ValueError, commands.ArgumentParsingError) as e:
                    await ctx.send("Bleh, smelled a bad argument.")

            else:
                await ctx.send("You're on cooldown.")

        # BAD ARGUMENTS
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send("Bleh, smelled a bad argument.")

        else:
            print(error)
            await ctx.send(str(error)[:1000])
            # error_message = traceback.format_exception(type(error), error, error.__traceback__)
            #
            # await ctx.send(
            #     f"Something just borked. Yup, it's an uncaught exception.\n"
            #     f"Pinging <@{constants.kat_id}> so she can fix this as soon as possible. \n\n"
            #     f"```{''.join([str(x) for x in error_message])}```"
            # )


def setup(bot):
    bot.add_cog(Handler(bot))
