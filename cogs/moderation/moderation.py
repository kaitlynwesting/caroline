import discord
from discord.ext import commands
from moderation_tools import animalise, mute, unmute, kick, ban, unban
from utils import constants


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["animalize", "forcenick"])
    @commands.has_permissions(kick_members=True)
    async def animalise(
            self,
            ctx,
            infraction_member: discord.Member,
            infraction_time,
            infraction_reason: str
    ):
        await animalise.animalise(
            ctx,
            infraction_member,
            infraction_time,
            infraction_reason,
        )

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
        Mutes a member for a specified amount of time. Time defaults to 7 days if not specified.
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

    @commands.command(aliases=["k"])
    @commands.has_permissions(kick_members=True)
    async def kick(
            self,
            ctx,
            infraction_member: discord.Member,
            *,
            infraction_reason="Your asshattery is not welcome here. Bye."
    ):
        await kick.kick(
            ctx,
            infraction_member,
            infraction_reason
        )

    @commands.command(aliases=["b"])
    @commands.has_permissions(kick_members=True)
    async def ban(
            self,
            ctx,
            infraction_member: discord.Member,
            *,
            infraction_reason="Your asshattery is not welcome here. Bye."
    ):
        await ban.ban(
            ctx,
            infraction_member,
            infraction_reason
        )

    @commands.command(aliases=["ub"])
    @commands.has_permissions(kick_members=True)
    async def unban(
            self,
            ctx,
            pardoned_member,
    ):
        await unban.unban(
            ctx,
            pardoned_member
        )


def setup(bot):
    bot.add_cog(Moderation(bot))
