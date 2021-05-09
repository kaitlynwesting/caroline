import discord
from discord.ext import commands


class Cleaner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, num: int, target: discord.User):
        if num > 500 or num < 0:
            return await ctx.send("Invalid amount. Maximum is 500.")

        def checker(m):
            if target is not None:
                return m.author.id == target.id
            return True

        try:
            deleted = await ctx.channel.purge(limit=num, check=checker)
            await ctx.channel.send(f'👌 Deleted {len(deleted)} message(s).')
        except discord.errors.NotFound as e:
            await ctx.channel.send(f'👌 Deleted message(s).')



    """ @commands.command()
    @commands.has_permissions(kick_members = True)
    async def wipe(self, ctx, amount=2, before=datetime.datetime.now(), after = datetime.datetime(2020, 5, 17)):
        await ctx.channel.purge(limit=amount + 1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True) 
    """


def setup(bot):
    bot.add_cog(Cleaner(bot))
