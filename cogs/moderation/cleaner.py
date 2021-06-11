import discord
from discord.ext import commands
from utils import constants


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


def setup(bot):
    bot.add_cog(Cleaner(bot))
