from discord.ext import commands
from discord.utils import get


# COG FOR NEW ARRIVALS AND DEPARTS

class Joins(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = get(member.guild.text_channels, name="logs")
        await channel.send(f"{member.mention} has joined us.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = get(member.guild.text_channels, name="logs")
        await channel.send(f"{member.mention} has left.")


def setup(bot):
    bot.add_cog(Joins(bot))
