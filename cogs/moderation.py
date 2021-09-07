import discord
from discord.ext import commands
from moderation_tools import warn, animalise, unanimalise, mute, unmute, kick, ban, unban
from cogs.utils import constants, embed_template


class Snipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.snipes = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.bot.snipes[message.channel.id] = message

    @commands.command(aliases=["deleted"])
    @commands.has_permissions(kick_members=True)
    async def snipe(self,
                    ctx,
                    *,
                    channel: discord.TextChannel = None
                    ):

        channel = ctx.channel if channel is None else channel

        try:
            message = self.bot.snipes[channel.id]
        except KeyError:
            return await ctx.send(f"Nothing to snipe from <#{channel.id}> since most recent deployment.")

        if not message.attachments:  # if there are no attachments

            await embed_template.server_embed_full(
                ctx.channel,
                f"{message.author.avatar_url}",
                f"Message author: {message.author}",
                f'',
                f"Last message deleted from: #{message.channel}:",
                f"{message.content}",
                f"",
                f"Deleted message was sent",
                message.created_at,
                constants.blurple,
            )
        else:
            attachments = message.attachments[0]

            await embed_template.server_embed_full(
                ctx.channel,
                f"{message.author.avatar_url}",
                f"Message author: {message.author}",
                f'',
                f"Last message deleted from: #{message.channel}:",
                f"{message.content}\n\n**Urls of attachments found:**\n{attachments.url}",
                f"{attachments.url}",
                f"Deleted message was sent",
                message.created_at,
                constants.blurple,
            )


class Cleaner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def purge_limit(self, ctx, limit, standard_limit):
        if limit < 0:
            await ctx.send(f"Invalid amount.")
            return False
        elif limit > standard_limit:
            await ctx.send(f"Can't do that. Maximum limit set for this mode is {standard_limit}.\n"
                           f"But check `!help purge` or its subcommands if you need.")
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
    @commands.group(invoke_without_command=True, aliases=["clean", "scrub", "delete", "deletus"])
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
            deleted_amount = await ctx.channel.purge(limit=limit+1)
            notification = await ctx.channel.send(f'👌 Deleted {len(deleted_amount)} message(s).')
            await notification.delete(delay=5)
        except Exception as e:
            notification = await ctx.channel.send(f'👌 Deleted messages. Caught an exception - {e} - for you.')
            await notification.delete(delay=5)

    @commands.dm_only()
    @purge.command(invoke_without_command=True, aliases=["clean", "scrub", "delete", "deletus"])
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
            deleted_amount = await ctx.channel.purge(limit=limit+1, check=checker)
            notification = await ctx.channel.send(f'👌 Deleted {len(deleted_amount)} message(s).')
            await notification.delete(delay=5)
        except Exception as e:
            notification = await ctx.channel.send(f'👌 Deleted messages. Caught an exception - {e} - for you.')
            await notification.delete(delay=5)


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["animalize", "anim", "forcenick", "fnick", "randimal", "jail", "imprison"])
    @commands.has_permissions(kick_members=True)
    async def animalise(
            self,
            ctx,
            infraction_member: discord.Member,
            infraction_time: str = '1d',
            *,
            infraction_reason: str = 'Your nickname was simply too terrible.'
    ):
        """
        Forcefully nicknames a member and prevents them from changing it for a period of time.
        Note: time defaults to 1 day if not specified.
        Example: !animalise 678576419596402691 10m Your name is too inappropriate

        :param ctx:
        :param infraction_member:
        :param infraction_time:
        :param infraction_reason: str
        :return:
        """

        await animalise.animalise(
            ctx,
            infraction_member,
            infraction_time,
            infraction_reason,
        )

    @commands.guild_only()
    @commands.command(aliases=["unanimalize", "unanim", "unjail", "release"])
    @commands.has_permissions(kick_members=True)
    async def unanimalise(
            self,
            ctx,
            pardoned_member: discord.Member,
    ):
        """
        Releases a member from nickname jail.
        Example: !unanimalise 678576419596402691

        :param ctx:
        :param pardoned_member: discord.Member
        :return:
        """

        await unanimalise.unanimalise(
            ctx,
            pardoned_member
        )

    @commands.guild_only()
    @commands.command(aliases=["w"])
    @commands.has_permissions(kick_members=True)
    async def warn(
            self,
            ctx,
            infraction_member: discord.Member,
            *,
            infraction_reason: str = None
    ):
        """
            Distributes a warning to a member.

            :param ctx: Context
            :param infraction_member: The member receiving the infraction. Discord object or ID
            :param infraction_reason: The infraction description and reason
            :return: None
        """

        await warn.warn(
            ctx,
            infraction_member,
            infraction_reason
        )

    @commands.guild_only()
    @commands.command(aliases=["m"])
    @commands.check_any(commands.has_role(constants.helper), commands.has_permissions(kick_members=True))
    async def mute(
            self,
            ctx,
            infraction_member: discord.Member,
            infraction_time="7d",
            *,
            infraction_reason="Being an idiot."
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
            ctx,
            infraction_member,
            infraction_time.lower(),
            infraction_reason
        )

    @commands.guild_only()
    @commands.command(aliases=["um"])
    @commands.check_any(commands.has_role(constants.helper), commands.has_permissions(kick_members=True))
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

        await unmute.unmute(
            ctx,
            pardoned_member
        )

    @commands.guild_only()
    @commands.command(aliases=["k"])
    @commands.has_permissions(kick_members=True)
    async def kick(
            self,
            ctx,
            infraction_member: discord.Member,
            *,
            infraction_reason="Your asshattery is not welcome here. Bye."
    ):
        """
        Kicks a member in the server.
        Example: !kick Kat Too cool

        :param ctx:
        :param infraction_member: discord.Member
        :param infraction_reason: str
        :return:
        """

        await kick.kick(
            ctx,
            infraction_member,
            infraction_reason
        )

    @commands.guild_only()
    @commands.command(aliases=["b"])
    @commands.has_permissions(kick_members=True)
    async def ban(
            self,
            ctx,
            infraction_member: discord.Member,
            *,
            infraction_reason="Your asshattery is not welcome here. Bye."
    ):
        """
        Bans a member in the server.
        Note: by default, this will also delete all of their messages.
        Example: !ban Kat Too cool

        :param ctx:
        :param infraction_member: discord.Member
        :param infraction_reason: str
        :return:
        """
        await ban.ban(
            ctx,
            infraction_member,
            infraction_reason
        )

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
        await unban.unban(
            ctx,
            pardoned_member
        )

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

        await(ctx.guild.ban(discord.Object(id=infraction_member_id)))
        await ctx.send("Done.")


def setup(bot):
    bot.add_cog(Snipe(bot))
    bot.add_cog(Cleaner(bot))
    bot.add_cog(Moderation(bot))
