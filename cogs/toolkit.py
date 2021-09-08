from discord.ext import commands
from cogs.utils import constants, embed_template


class Rules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # TOGGLE RULES FOR DUMMIES
    @commands.command(aliases=["rule"])
    async def rules(
            self,
            ctx,
            rule_number=0
    ):

        rule_text = getattr(constants, f"rule{rule_number}")

        await embed_template.server_embed(
            ctx.channel,
            f"Photoshop Discord Rules",
            f"**Rule {rule_number}**:\n"
            f"{rule_text}",
            f"",
            constants.blurple
        )

    @rules.error
    async def bounds_error(self, ctx, error):
        ctx.error_handled = True

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, AttributeError):
            await ctx.send(f"Rules range from 1-7.")
        else:
            ctx.error_handled = False


class Subscription(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["sub"])
    async def subscribe(self, ctx, subscription: str = None):
        """
        A commands for adding subscription role pings.

        :param ctx:
        :param subscription: str
        :return:
        """
        subscription_mapping = {'announcements': [constants.announcements_role],
                                'events': [constants.weekly_events_role]}

        if subscription is None:
            await ctx.send("What do you want to subscribe to? ")

        subscription_role = ctx.guild.get_role(subscription_mapping[subscription])

        if subscription_role in ctx.author.roles:
            return await ctx.send("You are already subscribed.")

        await ctx.author.add_roles(subscription_role)
        await ctx.send(f"{ctx.author.display_name}, you've joined our {subscription} subscription. Hurrah! \n"
                       f"You're able to unsubscribe at any time with `!unsubscribe`.")

    @commands.guild_only()
    @commands.command(aliases=["unsub"])
    async def unsubscribe(self, ctx, subscription: str = None):
        """
        A command to unsubscribe from a role ping.

        :param ctx:
        :param subscription: str
        :return:
        """
        subscription_mapping = {'announcements': [constants.announcements_role],
                                'events': [constants.weekly_events_role]}

        if subscription is None:
            await ctx.send("What do you want to unsubscribe from? ")

        subscription_role = ctx.guild.get_role(subscription_mapping[subscription])

        if subscription_role in ctx.author.roles:
            return await ctx.send("You are already subscribed.")

        await ctx.author.add_roles(subscription_role)
        await ctx.send(f"{ctx.author.display_name}, you've joined our {subscription} subscription. Hurrah! \n"
                       f"You're able to unsubscribe at any time with `!unsubscribe`.")


def setup(bot):
    bot.add_cog(Rules(bot))
    bot.add_cog(Subscription(bot))
