import discord
from discord.ext import commands


class Cleaner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

        if limit > 500 or limit < 0:
            return await ctx.send("Invalid amount. Maximum is 500.")

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
