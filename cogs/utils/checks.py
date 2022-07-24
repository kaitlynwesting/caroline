from discord.ext import commands
from cogs.utils import constants


def reply_check(ctx, message):
    return ctx.author.id == message.author.id and ctx.channel.id == message.channel.id


def staff_only():
    def predicate(ctx):
        helper = ctx.guild.get_role(constants.helper)
        moderator = ctx.guild.get_role(constants.mod)
        admin = ctx.guild.get_role(constants.admin)

        staff_roles = [helper, moderator, admin]

        staff = any(role in staff_roles for role in ctx.author.roles)

        return staff

    return commands.check(predicate)


def mod_only():
    def predicate(ctx):
        moderator = ctx.guild.get_role(constants.mod)
        admin = ctx.guild.get_role(constants.admin)

        mod_roles = [moderator, admin]

        staff = any(role in mod_roles for role in ctx.author.roles)

        return staff

    return commands.check(predicate)

