import discord
from discord.ext import commands
from cogs.utils import constants


class ActionReason(commands.Converter):
    """Appends mod name and delimits mod command reasons."""

    async def convert(self, ctx, argument):
        reason = f'{ctx.author} (ID: {ctx.author.id}): {argument}'

        if len(reason) > 512:
            reason_max = 512 - len(reason) + len(argument)  # without mod name
            raise commands.BadArgument(f'Reason is too long ({len(argument)}/{reason_max})')
        return reason


class Moderation(commands.Cog):
    """Moderation related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Mutes a members for a specified amount of time."""

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmutes a currently muted member."""

        return

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: ActionReason = None):
        """Kicks a member from the server."""

        if reason is None:
            reason = f"Action done by {ctx.author} (ID: {ctx.author.id})"

        await ctx.guild.kick(member, reason=reason)
        await ctx.send("\N{OK HAND SIGN}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User, days: int = 1, *, reason=None):
        """
        Bans a member from the server.

        You can also ban from ID to ban regardless whether they're
        in the server or not.
        """

        if reason is None:
            reason = f"Action done by {ctx.author} (ID: {ctx.author.id})"

        await ctx.guild.ban(member, delete_message_days=days, reason=reason)
        await ctx.send("\N{OK HAND SIGN}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def multiban(
            self, ctx, members: commands.Greedy[discord.User], *, reason=None
    ):
        """
        Bans multiple members from the server.
        This only works through banning via ID.
        """

        if reason is None:
            reason = f"Action done by {ctx.author} (ID: {ctx.author.id})"

        total_members = len(members)
        if total_members == 0:
            return await ctx.send("Missing members to ban.")

        confirm = await ctx.prompt(
            f"This will ban **{total_members}**. Are you sure?"
        )
        if not confirm:
            return await ctx.send("Aborting.")

        failed = 0
        for member in members:
            try:
                await ctx.guild.ban(member, reason=reason)
            except discord.HTTPException:
                failed += 1

        await ctx.send(f"Banned {total_members - failed}/{total_members} members.")

    @commands.guild_only()
    @commands.command(aliases=["ub"])
    @commands.has_permissions(kick_members=True)
    async def unban(
            self,
            ctx,
            pardoned_member,
    ):
        """
        Unbans a banned member.
        Note: directly insert ONLY the member's ID, otherwise the bot cannot convert.
        Example: !unban 669977303584866365

        :param ctx:
        :param pardoned_member:
        :return:
        """
        await unban.unban(ctx, pardoned_member)

    @commands.guild_only()
    @commands.command(aliases=["hb"])
    @commands.has_permissions(kick_members=True)
    async def hackban(
            self,
            ctx,
            infraction_member_id,
    ):
        """
        Bans a member not in the server.
        Note: directly insert ONLY the member's ID, otherwise the bot cannot convert.
        Example: !hackban 669977303584866365

        :param ctx:
        :param infraction_member_id: int
        :return:
        """

        await (ctx.guild.ban(discord.Object(id=infraction_member_id)))
        await ctx.send("Done.")


def setup(bot):
    bot.add_cog(Moderation(bot))
