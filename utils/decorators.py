from discord.ext import commands
from utils import constants


def is_staff():
    def predicate(ctx):
        helper = ctx.guild.get_role(constants.helper)
        moderator = ctx.guild.get_role(constants.mod)
        admin = ctx.guild.get_role(constants.admin)

        staff_roles = [helper, moderator, admin]

        return any(role in ctx.author.roles for role in staff_roles)
    return commands.check(predicate)
