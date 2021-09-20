import discord
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

        subscription_role = ctx.guild.get_role((subscription_mapping[subscription])[0])

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

        subscription_role = ctx.guild.get_role((subscription_mapping[subscription])[0])

        if subscription_role in ctx.author.roles:
            return await ctx.send("You are not subscribed, what is there to unsubscribe from?")

        await ctx.author.add_roles(subscription_role)
        await ctx.send(f"Successfully removed subscription.")


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        embed = discord.Embed(color=0x349feb)

        if member is None:
            member = ctx.author

        embed.set_image(url=member.avatar.url)
        embed.set_author(name=f"{member.display_name}'s avatar:", icon_url=member.avatar.url)

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def member(self, ctx, member: discord.Member = None):

        if member is None:
            member = ctx.author

        embed = discord.Embed(
            title=f"{member.display_name}",
            color=constants.blurple
        )

        embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(
            name=f"User information",
            value=f"Created: {member.created_at.strftime('%A, %B %d, %Y, at %H:%M')}\n"
                  f"Profile: {member.mention}\n"
                  f"ID: {member.id}",
            inline=False
        )

        role_list = []
        for role in member.roles:
            role_list.append(f"{role.mention}")

        embed.add_field(
            name=f"Member information",
            value=f"Joined at: {member.joined_at.strftime('%A, %B %d, %Y, at %H:%M')}\n"
                  f"Roles: {', '.join(role_list[1:])}\n",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def user(self, ctx, user: discord.User):

        embed = discord.Embed(
            title=f"{user}",
            color=constants.blurple
        )

        embed.set_thumbnail(url=user.avatar.url)

        embed.add_field(
            name=f"User information",
            value=f"Created: {user.created_at.strftime('%A, %B %d, %Y, at %H:%M')}\n"
                  f"Profile: {user.mention}\n"
                  f"ID: {user.id}",
            inline=False
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Rules(bot))
    bot.add_cog(Subscription(bot))
    bot.add_cog(User(bot))
