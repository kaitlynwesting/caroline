import discord
from discord.ext import commands

from utils import constants


class Subscription(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(aliases=["sub"], invoke_without_command=True)
    async def subscribe(self, ctx):
        """
        A group of commands for adding subscription role pings.

        :param ctx:
        :return:
        """
        print(str(ctx.subcommand_passed))
        if ctx.invoked_subcommand is None:

            await ctx.send("What do you want to subscribe to? "
                           "Choose a subcommand from the below menu.")

            await ctx.send_help('subscribe')

    @subscribe.command()
    async def announcements(self, ctx):
        print(ctx.author.name)

        announcements_role = ctx.guild.get_role(constants.announcements_role)

        if announcements_role in ctx.author.roles:
            await ctx.send("You are already subscribed.")
            return

        await ctx.author.add_roles(announcements_role)
        await ctx.send(f"{ctx.author.display_name}, you have joined our announcements subscription. "
                       "You may be notified occasionally of the server's news and updates. \n"
                       "If you wish to unsubscribe, you can do so at any time with `!unsub announcements`.")

    @subscribe.command()
    async def events(self, ctx):
        weekly_events_role = ctx.guild.get_role(constants.weekly_events_role)

        if weekly_events_role in ctx.author.roles:
            await ctx.send("You are already subscribed.")
            return

        await ctx.author.add_roles(weekly_events_role)
        await ctx.send(f"{ctx.author.display_name}, you have joined our weekly events subscription, rejoice. "
                       "You will be be notified usually 2 times a week: once for a new event, and once to vote. \n"
                       "If you wish to unsubscribe, you can do so at any time with `!unsub events`.")

    @commands.guild_only()
    @commands.command(aliases=["unsub"])
    async def unsubscribe(self, ctx, subscribed_content: str = None):
        """
        A command to unsubscribe from a role ping.

        :param ctx:
        :param subscribed_content:
        :return:
        """
        announcements_role = ctx.guild.get_role(constants.announcements_role)
        weekly_events_role = ctx.guild.get_role(constants.weekly_events_role)

        if subscribed_content == 'announcements':
            if announcements_role not in ctx.author.roles:
                return await ctx.send("You are already not subscribed. "
                                      "Perhaps you meant to unsubscribe from something else?")

            await ctx.author.remove_roles(announcements_role)
            return await ctx.send("You have been removed from the announcements subscription.")

        elif subscribed_content == 'events':
            if weekly_events_role not in ctx.author.roles:
                return await ctx.send("You are already not subscribed. "
                                      "Perhaps you meant to unsubscribe from something else?")

            await ctx.author.remove_roles(weekly_events_role)
            return await ctx.send("You have been removed from the weekly events subscription.")

        else:
            await ctx.send("Not a valid subscription to unsubscribe from. "
                           "Choose from one of the subcommands below.")
            return await ctx.send_help('unsubscribe')


def setup(bot):
    bot.add_cog(Subscription(bot))
