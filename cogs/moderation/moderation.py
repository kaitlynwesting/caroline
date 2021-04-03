import discord
from discord.ext import commands
from moderation_tools import warn, mute, unmute, kick, ban, unban


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases="w")
    @commands.has_permissions(kick_members=True)
    async def warn(
            self,
            ctx,
            infraction_member: discord.Member,
            infraction_reason=None
    ):

        await warn.warn(
            ctx,
            infraction_member,
            infraction_reason
        )

    @commands.command(aliases="m")
    @commands.has_permissions(kick_members=True)
    async def mute(
            self,
            ctx,
            infraction_member: discord.Member,
            infraction_time,
            *,
            infraction_reason=None
    ):

        # If there is no number in the infraction_time parameter, one can assume that no argument has been passed
        # to infraction_time. Therefore, the default infraction_time would then be 7d.

        if not any(char.isdigit() for char in infraction_time):
            infraction_reason = f"{infraction_time} {infraction_reason}"
            infraction_time = "7d"

        await mute.mute(
            ctx,
            infraction_member,
            infraction_time,
            infraction_reason
        )

    @commands.command(aliases="um")
    @commands.has_permissions(kick_members=True)
    async def unmute(
            self,
            ctx,
            pardoned_member: discord.Member,
    ):

        await unmute.unmute(
            ctx,
            pardoned_member
        )

    @commands.command(aliases="k")
    @commands.has_permissions(kick_members=True)
    async def kick(
            self,
            ctx,
            infraction_member: discord.Member,
    ):
        await kick.kick(
            ctx,
            infraction_member
        )

    @commands.command(aliases="b")
    @commands.has_permissions(kick_members=True)
    async def ban(
            self,
            ctx,
            infraction_member: discord.Member,
    ):
        await ban.ban(
            ctx,
            infraction_member
        )

    @commands.command(aliases="ub")
    @commands.has_permissions(kick_members=True)
    async def unban(
            self,
            ctx,
            pardoned_member: discord.Member,
    ):
        await unban.unban(
            ctx,
            pardoned_member
        )


def setup(bot):
    bot.add_cog(Moderation(bot))
