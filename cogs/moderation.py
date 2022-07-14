import discord
from discord.ext import commands
from cogs.utils.time_converter import format_timedelta


class ActionReason(commands.Converter):
    """Appends mod name and character limits mod command reasons."""

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

    class PurgeFlags(commands.FlagConverter, prefix='--', delimiter=' '):
        amount: int = 100
        channel: discord.TextChannel = None
        chars: int = 0
        contains: str = ""
        target: discord.User = None

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, *, flags: PurgeFlags):
        """
        A mini flag-based purger.

        --amount: amount of messages to scan. Defaults to 100.
        --channel: channel to purge. Defaults to current channel.
        --chars: minimum characters in message for purging.
        --contains: specific phrase in message.
        --target: specific user's messages.
        """

        if flags.channel is None:
            flags.channel = ctx.channel

        if int(flags.amount) > 500:
            return await ctx.send(f'Exceeds purge limit of 500 messages.')

        confirm = await ctx.prompt(
            f"This will scan {flags.amount} messages in {flags.channel}. Are you sure? "
        )
        if not confirm:
            return await ctx.send("Aborting.")

        await ctx.message.delete()

        def check(message: discord.Message) -> bool:
            if 0 < flags.chars > len(message.content):
                return False

            if flags.contains and flags.contains not in message.content:
                return False

            if flags.target:
                return message.author == flags.target
            return True

        num = await flags.channel.purge(limit=flags.amount, check=check)

        await ctx.send(f'Deleted the last {len(num)}/{flags.amount} messages.')

    @commands.command(aliases=['timeout'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, members: commands.Greedy[discord.Member], timespan: str, *, reason: ActionReason = None):
        """Mutes a list of members using timeout feature."""

        total_members = len(members)
        if total_members == 0:
            return await ctx.send("Missing members to ban.")

        failed = 0

        for member in members:
            try:
                await member.timeout(format_timedelta(timespan), reason=reason)
            except discord.HTTPException:
                failed += 1

        await ctx.send(f'\N{OK HAND SIGN} Muted {total_members - failed}/{total_members} members.')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, members: commands.Greedy[discord.Member]):
        """Unmutes a list of currently muted members."""

        total_members = len(members)
        if total_members == 0:
            return await ctx.send("Missing members to ban.")

        failed = 0

        for member in members:
            try:
                await member.timeout(None)
            except discord.HTTPException:
                failed += 1

        await ctx.send(f'\N{OK HAND SIGN} Unmuted {total_members - failed}/{total_members} members.')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: ActionReason = None):
        """Kicks a member from the server."""

        if reason is None:
            reason = f"Action done by {ctx.author} (ID: {ctx.author.id})"

        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"\N{OK HAND SIGN} Kicked {member}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User, *, reason: ActionReason = None):
        """
        Bans a member from the server.

        Can also ban from ID to ban regardless whether they're in the server or not.
        """

        if reason is None:
            reason = f"Action done by {ctx.author} (ID: {ctx.author.id})"

        await ctx.guild.ban(member, delete_message_days=1, reason=reason)
        await ctx.send(f"\N{OK HAND SIGN} Banned {member}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def multiban(
            self, ctx, members: commands.Greedy[discord.User], *, reason: ActionReason = None
    ):
        """
        Bans multiple members from the server.

        This only works through banning via ID.
        """
        total_members = len(members)

        if total_members == 0:
            return await ctx.send("Missing members to ban.")

        if reason is None:
            reason = f"Action done by {ctx.author} (ID: {ctx.author.id})"

        confirm = await ctx.prompt(
            f"This will ban **{total_members}** members. Are you sure?"
        )
        if not confirm:
            return await ctx.send("Aborting.")

        failed = 0
        for member in members:
            try:
                await ctx.guild.ban(member, reason=reason)
            except discord.HTTPException:
                failed += 1

        await ctx.send(f"\N{OK HAND SIGN} Banned {total_members - failed}/{total_members} members.")

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
