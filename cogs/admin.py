import aiohttp
import discord
from discord.ext import commands


class Admin(commands.Cog):
    """A collection of admin-only commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def sql(self, ctx, *, query: str):
        """Executes some sql. (fetch)"""

        rows = await self.bot.db.execute(query)
        rows = await rows.fetchall()

        await ctx.send(rows)

        # rows = await self.bot.db.execute("""SELECT * FROM users WHERE user_id = ?""", (ctx.member.id,))
        # rows = await rows.fetchall()


def setup(bot):
    bot.add_cog(Admin(bot))
