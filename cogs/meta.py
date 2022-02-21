import discord
from discord import Embed
from discord.ext import commands
from cogs.utils import constants, embed_template


class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rule"])
    async def rules(self, ctx, rule_number=0):

        rule_text = getattr(constants, f"rule{rule_number}")

        await embed_template.server_embed(
            ctx.channel,
            f"Photoshop Discord Rules",
            f"**Rule {rule_number}**:\n" f"{rule_text}",
            f"",
            constants.blurple,
        )

    @rules.error
    async def bounds_error(self, ctx, error):
        ctx.error_handled = True

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, AttributeError):
            await ctx.send(f"Rules range from 1-10.")
        else:
            ctx.error_handled = False


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(color=discord.Color.blurple())
        embed.set_image(url=member.avatar.url)
        embed.set_author(
            name=f"{member.display_name}'s avatar:", icon_url=member.avatar.url
        )

        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def profile(self, ctx, member: discord.Member = None):
        """
        Manages a member's profile information.

        If called without a subcommand, this will display a member's profile.
        """

        if member is None:
            member = ctx.author

        query = """INSERT INTO users (user_id)
                   VALUES (?)
                   ON CONFLICT(user_id)
                   DO NOTHING
                """

        await self.bot.db.execute(query, (member.id,))
        await self.bot.db.commit()

        query = """SELECT * 
                   FROM users 
                   WHERE user_id = ?
                """

        rows = await self.bot.db.execute(query, (member.id,))
        rows = await rows.fetchall()

        embed = Embed.from_dict({'title': f"{member.display_name}'s {ctx.guild.name} profile",
                                 'thumbnail': {'url': f'{member.avatar.url}'},
                                 'color': constants.blurple,
                                 'fields': [
                                     {'name': 'About me',
                                      'value': f'{rows[0][1]}',
                                      'inline': False},
                                     {'name': 'Server info',
                                      'value': f'Reputation: {rows[0][2]}\n'
                                               f'Created at: {member.created_at.strftime("%A, %B %d, %Y, at %H:%M")}\n'
                                               f'Joined at: {member.joined_at.strftime("%A, %B %d, %Y, at %H:%M")}\n',
                                      'inline': False}
                                 ],
                                 # 'footer': {'text': 'Use help profile to see how to edit your profile'},
                                 })

        # embed.add_field(
        #     name=f"User information",
        #     value=f"Created: {member.created_at.strftime('%A, %B %d, %Y, at %H:%M')}\n"
        #           f"Profile: {member.mention}\n"
        #           f"ID: {member.id}",
        #     inline=False)

        await ctx.send(embed=embed)

    @profile.command()
    @commands.guild_only()
    async def about(self, ctx, *, about):
        """Edit your About Me profile."""

        query = """UPDATE users 
                   SET about = (?)
                   WHERE user_id = (?)
                """

        await self.bot.db.execute(query, (about, ctx.author.id,))
        await self.bot.db.commit()

        await ctx.send("Done.")


def setup(bot):
    bot.add_cog(Rules(bot))
    bot.add_cog(Meta(bot))
