import discord
import aiohttp
from asyncio import TimeoutError
from discord import Embed
from discord.ext import commands
from cogs.utils import constants
from cogs.utils.formats import LengthLimiter


class NoDmsEnabled(commands.CommandError):
    def __init__(self):
        super().__init__('I could not DM you. Please consider enabling DMs temporarily for this server and retrying.')


# class NoWork(HTTPException):
#     """All kinds of reasons for why this request is not working."""
#     def __init__(self, message: str = None):
#         super().__init__(reason='No Work')
#         self.destination


class Meta(commands.Cog):
    """Utilities relating to the server or a user."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rule"])
    async def rules(self, ctx, rule_number=0):
        """Check the rules of the server."""

        # Works ok but I don't really like this

        rule_text = getattr(constants, f"rule{rule_number}")

        embed = Embed.from_dict({'title': f"{ctx.guild.name} Rules",
                                 # 'description': f'**Rule {rule_number}**: \n'
                                 #                f'{rule_text}',
                                 'fields': [{'name': f'Rule {rule_number}',
                                             'value': f'{rule_text}',
                                             'inline': True}],
                                 'color': discord.Color.og_blurple().value
                                 })

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
                                 'color': discord.Color.og_blurple().value,
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

        # Optional: social accounts
        if rows[0][3] is not None:  # instagram column
            embed.add_field(
                name=f"Verified social accounts",
                value=f"Instagram: @{rows[0][3]}\n",
                inline=False)

        await ctx.send(embed=embed)

    @profile.command()
    @commands.guild_only()
    async def about(self, ctx, *, about: LengthLimiter):
        """Edit the About Me section of your profile."""

        query = """UPDATE users 
                   SET about = (?)
                   WHERE user_id = (?)
                """

        await self.bot.db.execute(query, (about, ctx.author.id,))
        await self.bot.db.commit()

        await ctx.send("Updated About Me in your server profile.")

    @profile.command(aliases=['ig'])
    async def instagram(self, ctx):
        """
        Verify your Instagram account with oauth. (Temporary implementation)
        """

        # Optimistically, we would have a Django website also connected to the same db on the same server;
        # too much room for user error by outsourcing work to the human

        try:
            dms = await ctx.author.create_dm()  # use this DM ctx object
            await ctx.author.send(f'We will verify your Instagram account with oauth. By signing in to Instagram and '
                                  f'granting us permission to view basic account information, we will be able to '
                                  f'verify that you own the account. Authentication is handled through Instagram; '
                                  f'we cannot see your password. \n\n'
                                  f'**Use the following link to sign in: **'
                                  f'https://photoshoppark.herokuapp.com/instagram-auth \n'
                                  f'**A detailed introduction to oauth: **'
                                  f'Introduction to oauth: https://oauth.net/about/introduction/')
        except discord.Forbidden:
            raise NoDmsEnabled from None

        def check(msg):
            return msg.author == ctx.author and msg.guild is None

        try:
            cat = await self.bot.wait_for('message', timeout=300.0, check=check)
        except TimeoutError:
            return await dms.send('You took long to verify. Aborting.')

        cat = cat.content.split('.')

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"https://graph.instagram.com/{cat[0]}?fields=id,username&access_token={cat[1]}") as response:
                    if response.status >= 400:  # usually bad id or token, less commonly network
                        return await dms.send('```That was unsuccessful.```')

                    info = await response.json()
                    print(info)

                    query = """UPDATE users 
                               SET instagram_username = (?)
                               WHERE user_id = (?)
                            """

                    await self.bot.db.execute(query, (info['username'], ctx.author.id,))
                    await self.bot.db.commit()

                    await ctx.send("Updated Instagram in your server profile.")

        except IndexError:
            await dms.send('```Bad format. Make sure to copy the entire code.```')


def setup(bot):
    bot.add_cog(Meta(bot))
