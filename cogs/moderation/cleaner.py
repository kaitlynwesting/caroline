import discord
from discord.ext import commands
from utils import constants


class Cleaner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def purge_limit(self, ctx, limit, standard_limit):
        if limit < 0:
            return await ctx.send(f"Invalid amount.")
        elif limit > standard_limit:
            return await ctx.send(f"Can't do that. Maximum limit set for this mode is {standard_limit}.\n"
                                  f"But check `!help purge` or its subcommands if you need.")

    async def purge_logger(self, ctx, limit):
        logs = self.bot.get_channel(constants.logs)
        kat = self.bot.get_user(constants.kat_id)
        purged_messages_list = await ctx.channel.history(limit=limit).flatten()

        logs.send(f"{ctx.author}: `{ctx.message.content}`")
        kat.send(purged_messages_list)

        return

    @commands.guild_only()
    @commands.group(invoke_without_command=True, aliases=["clean", "scrub", "delete", "deletus"])
    @commands.has_permissions(kick_members=True)
    async def purge(self, ctx, limit: int = 2):
        """
        Purges the most recent number of messages from a channel. No filters are applied.
        Note: limit will default to 1, if limit is not specified.
        Example: !purge 10

        :param ctx:
        :param limit: int = 1
        :return:
        """

        self.purge_limit(ctx, limit, standard_limit=50)
        self.purge_logger(ctx, limit)

        try:
            deleted_amount = await ctx.channel.purge(limit=limit)
            notification = await ctx.channel.send(f'👌 Deleted {len(deleted_amount)} message(s).')
            await notification.delete(delay=5)
        except Exception as e:
            notification = await ctx.channel.send(f'👌 Deleted messages. Caught an exception - {e} - for you.')
            await notification.delete(delay=5)

    @commands.guild_only()
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

        self.purge_limit(ctx, limit, standard_limit=50)
        self.purge_logger(ctx, limit)

        def checker(m):
            return m.author.id == purged_user.id

        try:
            deleted_amount = await ctx.channel.purge(limit=limit, check=checker)
            notification = await ctx.channel.send(f'👌 Deleted {len(deleted_amount)} message(s).')
            await notification.delete(delay=5)
        except Exception as e:
            notification = await ctx.channel.send(f'👌 Deleted messages. Caught an exception - {e} - for you.')
            await notification.delete(delay=5)



def setup(bot):
    bot.add_cog(Cleaner(bot))
