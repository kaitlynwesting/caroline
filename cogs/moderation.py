import discord
from discord.ext import commands
from cogs.utils import constants, embed_template


class Cleaner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def purge_limit(self, ctx, limit, standard_limit):
        if limit < 0:
            await ctx.send(f"Invalid amount.")
            return False
        elif limit > standard_limit:
            await ctx.send(
                f"Can't do that. Maximum limit set for this mode is {standard_limit}.\n"
                f"But check `!help purge` or its subcommands if you need."
            )
            return False
        else:
            return True

    async def purge_logger(self, ctx, limit):
        logs = self.bot.get_channel(constants.logs)
        kat = self.bot.get_user(constants.kat_id)
        purged_messages_raw = await ctx.channel.history(limit=limit).flatten()

        def content(raw_message):
            return f"**{raw_message.author}**: {raw_message.content}"

        purged_messages = list(map(content, purged_messages_raw))

        await kat.send(f"**Purged message log**")
        for message in purged_messages[::-1]:
            await kat.send(message)
        await kat.send(f"**Fin**")

        return

    @commands.guild_only()
    @commands.group(
        invoke_without_command=True, aliases=["clean", "scrub", "delete", "deletus"]
    )
    @commands.has_permissions(kick_members=True)
    async def purge(self, ctx, limit: int = 2):
        """
        Purges the most recent number of messages from a channel. No filters are applied.
        Example: !purge 10

        :param ctx:
        :param limit: int = 2
        :return:
        """

        if await self.purge_limit(ctx, limit, standard_limit=50) is False:
            return

        try:
            deleted_amount = await ctx.channel.purge(limit=limit + 1)
            notification = await ctx.channel.send(
                f"👌 Deleted {len(deleted_amount)} message(s)."
            )
            await notification.delete(delay=5)
        except Exception as e:
            notification = await ctx.channel.send(
                f"👌 Deleted messages. Caught an exception - {e} - for you."
            )
            await notification.delete(delay=5)

    @purge.command(
        invoke_without_command=True, aliases=["clean", "scrub", "delete", "deletus"]
    )
    @commands.has_permissions(kick_members=True)
    async def user(self, ctx, purged_user: discord.User, limit: int = None):
        """
        Purges messages from a specific user.
        Note: limit refers to HOW MANY messages the bot should scan. It does not refer to how many messages to delete
        from a person.
        Note: if target_member is not specified, the bot will delete messages from a channel regardless of the author.
        Example: !purge 100 669977303584866365 # Scans last 100 messages in a channel, and delete any messages from
        user with ID 669977303584866365

        :param ctx:
        :param purged_user: discord.Member
        :param limit: int
        :return:
        """

        if await self.purge_limit(ctx, limit, standard_limit=50) is False:
            return

        def checker(m):
            return m.author.id == purged_user.id

        try:
            deleted_amount = await ctx.channel.purge(limit=limit + 1, check=checker)
            notification = await ctx.channel.send(
                f"👌 Deleted {len(deleted_amount)} message(s)."
            )
            await notification.delete(delay=5)
        except Exception as e:
            notification = await ctx.channel.send(
                f"👌 Deleted messages. Caught an exception - {e} - for you."
            )
            await notification.delete(delay=5)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["w"])
    @commands.has_permissions(kick_members=True)
    async def warn(
            self, ctx, infraction_member: discord.Member, *, infraction_reason: str = None
    ):
        """
        Warns a member.

        :param ctx: Context
        :param infraction_member: The member receiving the infraction. Discord object or ID
        :param infraction_reason: The infraction description and reason
        :return: None
        """

        await warn.warn(ctx, infraction_member, infraction_reason)

    @commands.guild_only()
    @commands.command(aliases=["m"])
    @commands.check_any(
        commands.has_role(constants.helper), commands.has_permissions(kick_members=True)
    )
    async def mute(
            self,
            ctx,
            infraction_member: discord.Member,
            infraction_time="7d",
            *,
            infraction_reason="Being an idiot.",
    ):
        """
        Mutes a member for a specified amount of time.
        Note: time defaults to 7 days if not specified.
        Example: !mute Kat 10m Too cool

        :param ctx: Context
        :param infraction_member: discord.Member
        :param infraction_time: str
        :param infraction_reason: str
        :return:
        """

        # If there is no number in the infraction_time parameter, one can assume that no argument has been passed
        # to infraction_time. Therefore, the default infraction_time would then be 7d.

        if not any(char.isdigit() for char in infraction_time):
            infraction_reason = f"{infraction_time} {infraction_reason}"
            infraction_time = "7d"

        await mute.mute(
            ctx, infraction_member, infraction_time.lower(), infraction_reason
        )

    @commands.guild_only()
    @commands.command(aliases=["um"])
    @commands.check_any(
        commands.has_role(constants.helper), commands.has_permissions(kick_members=True)
    )
    async def unmute(
            self,
            ctx,
            pardoned_member: discord.Member,
    ):
        """
        Unmutes a currently muted member.
        Example: !unmute Kat

        :param ctx: Context
        :param pardoned_member: discord.Member
        :return:
        """

        await unmute.unmute(ctx, pardoned_member)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(
            self,
            ctx,
            member: discord.Member,
            *,
            reason=None,
    ):
        """
        Kicks a member from the server.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await ctx.guild.kick(member, reason=reason)
        await ctx.send("\N{OK HAND SIGN}")

    @commands.guild_only()
    @commands.command(aliases=["b"])
    @commands.has_permissions(kick_members=True)
    async def ban(
            self,
            ctx,
            member: discord.User,
            *,
            delete_message_days: int = 1,
            reason=None,
    ):
        """
        Bans a member from the server.

        You can also ban from ID to ban regardless whether they're
        in the server or not.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await ctx.guild.ban(member, delete_message_days, reason=reason)
        await ctx.send('\N{OK HAND SIGN}')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def multiban(self, ctx, members: commands.Greedy[discord.User], *, reason=None):
        """Bans multiple members from the server.
        This only works through banning via ID.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permission.
        """

        if reason is None:
            reason = f"Action done by {ctx.author} (ID: {ctx.author.id})"

        total_members = len(members)
        if total_members == 0:
            return await ctx.send("Missing members to ban.")

        confirm = await ctx.prompt(
            f"This will ban **{(total_members):member}**. Are you sure?",
            reacquire=False,
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
    bot.add_cog(Snipe(bot))
    bot.add_cog(Cleaner(bot))
    bot.add_cog(Moderation(bot))
