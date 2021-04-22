import discord
from discord.ext import commands
from discord.utils import get

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
            await ctx.send("You can't. Why?", file=discord.File("./media/image1.jpg"))

        # CAN'T FIND COMMAND
        elif isinstance(error, commands.CommandNotFound):

            if not ctx.message.content.startswith("!d"):

                await ctx.send("Couldn't find that command, sorry.")

        # CAN'T FIND PERSON
        elif isinstance(error, commands.MemberNotFound):

            await ctx.send(
                "Couldn't find anyone, sorry. \n"
                "To successfully convert someone to a `discord.Member` object, "
                "use their ID, mention, or name."
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
            error_message = traceback.format_exception(type(error), error, error.__traceback__)

            await ctx.send(
                f"Something just borked. Yup, it's an uncaught exception.\n"
                f"You should probably scream at Kat now so she can fix me. (I kid, please don't shriek) \n\n"
                f"```{''.join([str(x) for x in error_message])}```"
                f"If you're the first person to have seen this type of error, {ctx.author.name}, congratulations! "
                f"Uncaught exceptions are rare, and you deserve to be rewarded for your contribution to bug hunting."
            )


def setup(bot):
    bot.add_cog(Handler(bot))
