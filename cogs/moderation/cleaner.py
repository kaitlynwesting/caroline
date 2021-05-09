import discord
from discord.ext import commands


class Cleaner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int, target_member: discord.User):
        """
        Clears messages.
        Note: limit refers to HOW MANY messages the bot should scan. It does not refer to how many messages to delete
        from a person.
        Note: if target_member is not specified, the bot will delete messages from a channel regardless of the author.
        Example: !purge 100 669977303584866365 # Scans last 100 messages in a channel, and delete any messages from
        user with ID 669977303584866365

        :param ctx:
        :param limit: int
        :param target_member: discord.Member
        :return:
        """

        if limit > 500 or limit < 0:
            return await ctx.send("Invalid amount. Maximum is 500.")

        def checker(m):
            if target_member is not None:
                return m.author.id == target_member.id
            return True

        try:
            deleted = await ctx.channel.purge(limit=limit, check=checker)
            await ctx.channel.send(f'👌 Deleted {len(deleted)} message(s).')
        except discord.errors.NotFound as e:
            await ctx.channel.send(f'👌 Deleted messages. Caught {e} for you.')



    """ @commands.command()
    @commands.has_permissions(kick_members = True)
    async def wipe(self, ctx, amount=2, before=datetime.datetime.now(), after = datetime.datetime(2020, 5, 17)):
        await ctx.channel.purge(limit=amount + 1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True) 
    """


def setup(bot):
    bot.add_cog(Cleaner(bot))
