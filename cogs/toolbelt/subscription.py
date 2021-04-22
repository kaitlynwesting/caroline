import discord
from discord.ext import commands
from discord.utils import get

from utils import constants


class Subscription(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # SUBSCRIBE ALL
    @commands.command(aliases=["sub"])
    async def subscribe(self, ctx, message):
        message = message.lower()

        if ctx.channel.id == constants.bot_commands:

            if message == "announcements":

                announce = ctx.guild.get_role(constants.announcements_sub)

                if announce in ctx.author.roles:  # check if they already have role
                    await ctx.send(f"You have already subscribed to this!")
                else:
                    await ctx.author.add_roles(announce)
                    await ctx.send(
                        f"{ctx.author.display_name}, you've subscribed to our announcements updates!")  # tag actual channel here in real server

            else:
                await ctx.send("Hmm, we don't offer that subscription yet. Perhaps you meant something else?")

        else:
            channel = get(ctx.guild.channels, name="bot-commands")
            await ctx.send(
                f"Please subscribe in the proper channel - that is, <#{constants.bot_commands}>.")  # UPDATE FOR REAL PS SERVER

    @commands.command()
    async def unsubscribe(self, ctx, message):
        message = message.lower()

        if ctx.channel.name == "bot-commands":
            if (message == "totd"):
                totd = get(ctx.guild.roles, name="Tip of the Day")

                if totd in ctx.author.roles:  # check if they already have role
                    await ctx.author.remove_roles(totd)
                    await ctx.send(f"{ctx.author.display_name}, you've successfully unsubscribed from our daily tips!")
                else:
                    await ctx.send(
                        f"You're not a subscriber. What is there to unsubscribe from?")  # tag actual channel here in real server

            elif (message == "announcements"):
                announce = get(ctx.guild.roles, name="Announcements")

                if announce in ctx.author.roles:  # check if they already have role
                    await ctx.author.remove_roles(announce)
                    await ctx.send(
                        f"{ctx.author.display_name}, you've successfully unsubscribed from our announcements!")
                else:
                    await ctx.send(f"You're not a subscriber. What is there to unsubscribe from?")
            else:
                await ctx.send("That's not a valid subscription.")

        else:
            channel = get(ctx.guild.channels, name="bot-commands")
            await ctx.send(
                f"Please unsubscribe in the proper channel - that is, <#{channel.id}>.")  # UPDATE FOR REAL PS SERVER


def setup(bot):
    bot.add_cog(Subscription(bot))
