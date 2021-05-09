import discord
from discord.ext import commands
from utils import constants
import datetime


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        embed = discord.Embed(color=0x349feb)

        if member is None:
            member = ctx.author

        embed.set_image(url=member.avatar_url)
        embed.set_author(name=f"{member.display_name}'s avatar:", icon_url=member.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def member(self, ctx, member: discord.Member = None):

        if member is None:
            member = ctx.author

        embed = discord.Embed(
            title=f"{member.nick} ({member})",
            color=constants.blurple
        )

        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(
            name=f"User information",
            value=f"Created: {member.created_at.strftime('%A, %B %d, %Y, at %H:%M')}\n"
                  f"Profile: {member.mention}\n"
                  f"ID: {member.id}",
            inline=False
        )

        role_list = []
        for role in member.roles:
            role_list.append(f"{role.mention}")

        embed.add_field(
            name=f"Member information",
            value=f"Joined at: {member.joined_at.strftime('%A, %B %d, %Y, at %H:%M')}\n"
                  f"Roles: {', '.join(role_list[1:])}\n",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def user(self, ctx, user: discord.User):

        embed = discord.Embed(
            title=f"{user}",
            color=constants.blurple
        )

        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(
            name=f"User information",
            value=f"Created: {user.created_at.strftime('%A, %B %d, %Y, at %H:%M')}\n"
                  f"Profile: {user.mention}\n"
                  f"ID: {user.id}",
            inline=False
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(User(bot))
