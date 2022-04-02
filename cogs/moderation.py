import discord
from discord.ext import commands
from cogs.utils import constants


class ActionReason(commands.Converter):
    """Appends mod name and limits mod command reasons."""

    async def convert(self, ctx, argument):
        reason = f'{ctx.author} (ID: {ctx.author.id}): {argument}'

        if len(reason) > 512:
            reason_max = 512 - len(reason) + len(argument)  # without mod name
            raise commands.BadArgument(f'Reason is too long ({len(argument)}/{reason_max})')
        return reason


class BannedMember(commands.Converter):
    """Checks if a member is a banned member."""

    async def convert(self, ctx, argument):
        member_id = int(argument, base=10)
        try:
            return await ctx.guild.fetch_ban(discord.Object(id=member_id))
        except discord.NotFound:
            raise commands.BadArgument('This member is not banned.') from None


class Moderation(commands.Cog):
    """Moderation related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, members: commands.Greedy[discord.Member], *, reason: ActionReason = None):
        """Mutes a list of members."""

        role = discord.Object(id=constants.muted)

        total = len(members)

        if total == 0:
            return await ctx.send('Missing members to mute.')

        failed = 0
        for member in members:
            try:
                await member.add_roles(role, reason=reason)
            except discord.HTTPException:
                failed += 1

        if failed == 0:
            await ctx.send('\N{THUMBS UP SIGN}')
        else:
            await ctx.send(f'Muted [{total - failed}/{total}] members.')

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
    async def ban(self, ctx, member: discord.User, *, reason: ActionReason = None):
        """
        Bans a member from the server.

        You can also ban from ID to ban regardless whether they're
        in the server or not.
        """

        if reason is None:
            reason = f"Action done by {ctx.author} (ID: {ctx.author.id})"

        await ctx.guild.ban(member, delete_message_days=1, reason=reason)
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

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: BannedMember, reason: ActionReason = None):
        """Unbans a banned member from the server."""

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await ctx.guild.unban(member, reason=reason)
        await ctx.send(f'\N{OK HAND SIGN} Unbanned {member}.')


async def setup(bot):
    await bot.add_cog(Moderation(bot))
