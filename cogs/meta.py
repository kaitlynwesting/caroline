import aiohttp
import discord
import random
import string
from asyncio import TimeoutError
from bs4 import BeautifulSoup as soup
from discord import Embed
from discord.ext import commands
from cogs.utils import constants
from cogs.utils.checks import staff_only
from cogs.utils.formats import LengthLimiter


def fetch(html_data):
    parsed = soup(html_data, "lxml")
    return parsed


def generate_code():
    """Generates an 8 character verification code."""
    code = f"psp{''.join(random.choice(string.digits) for i in range(5))}"
    return code


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

    @commands.command()
    async def flip(self, ctx):
        await ctx.send(random.choice(['Tails', 'Heads']))

    @commands.command()
    async def ping(self, ctx):
        """Check the latency of the bot."""
        await ctx.send(f"Pong! Latency is {round(self.bot.latency * 1000, 2)} ms.")

    @commands.command(aliases=["rule"])
    async def rules(self, ctx, rule_number=0):
        """Check the rules of the server."""

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

        verified = ctx.guild.get_role(constants.helper)

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
        rows = await rows.fetchone()

        ratings = await self.bot.db.execute(
            """SELECT AVG(stars), COUNT(completed) FROM commissions WHERE seller_id = (?)""", (member.id,))
        ratings = await ratings.fetchone()

        if verified in ctx.author.roles:

            if ratings[0] is not None:
                ratings[0] = round(ratings[0], 2)
            else:
                ratings[0] = None
        else:
            ratings = (None, 0)

        embed = Embed.from_dict({'title': f"{member.display_name}'s {ctx.guild.name} profile",
                                 'thumbnail': {'url': f'{member.avatar.url}'},
                                 'color': discord.Color.og_blurple().value,
                                 'fields': [
                                     {'name': 'About me',
                                      'value': f'{rows[1]}',
                                      'inline': False},
                                     {'name': 'Server info',
                                      'value': f'Reputation: {rows[2]}\n'
                                               f'Average Seller Rating: {ratings[0]}\n'
                                               f'Completed Commissions: {ratings[1]}\n'
                                               f'Created at: {discord.utils.format_dt(member.created_at)}\n'
                                               f'Joined at: {discord.utils.format_dt(member.joined_at)}\n',
                                      'inline': False}
                                 ],
                                 # 'footer': {'text': 'Use help profile to see how to edit your profile'},
                                 })

        # Optional: social accounts
        if all(i is None for i in rows[4:6]):  # this check the social media columns
            return await ctx.send(embed=embed)

        desc = ""
        mapping = {0: f"Instagram: [@{rows[4]}](https://www.instagram.com/{rows[4]})",
                   1: f"Behance: [@{rows[5]}](https://www.behance.net/{rows[5]})"}

        for num, i in enumerate(rows[4:6]):
            if i is not None:
                desc = f"{desc}{mapping[num]}\n"

        embed.add_field(
            name=f"Verified social accounts",
            value=desc,
            inline=False)

        await ctx.send(embed=embed)

    @profile.command()
    @commands.guild_only()
    async def about(self, ctx, *, about: LengthLimiter):
        """Edit the About Me section of your profile."""

        query = """INSERT INTO users (user_id, about)
                   VALUES (?, ?) 
                   ON CONFLICT (user_id)
                   DO UPDATE SET about = excluded.about
                """

        await self.bot.db.execute(query, (ctx.author.id, about,))
        await self.bot.db.commit()

        await ctx.send("Updated About Me in your server profile.")

    @profile.command(aliases=['ig'], hidden=True)
    async def instagram(self, ctx):
        """Verify your Instagram account with oauth. (Temporary implementation)"""

        # Optimistically, we would have a Django website also connected to the same db on the same server;
        # too much room for user error by outsourcing work to the human
        # Try to not DM in the future

        try:
            dms = await ctx.author.create_dm()  # use this DM ctx object
            await ctx.author.send(f'We will verify your Instagram account with oauth. By signing in to Instagram and '
                                  f'granting us permission to view basic account information, we will be able to '
                                  f'verify that you own the account. Authentication is handled through Instagram; '
                                  f'we cannot see your password. \n\n'
                                  f'**Use the following link to sign in: **'
                                  f'https://photoshoppark.herokuapp.com/instagram-auth \n'
                                  f'**A detailed introduction to oauth: **'
                                  f'https://oauth.net/about/introduction/')
        except discord.Forbidden:
            raise NoDmsEnabled from None

        def check(msg):
            return msg.author == ctx.author and msg.guild is None

        try:
            cat = await self.bot.wait_for('message', timeout=300.0, check=check)
        except TimeoutError:
            return await dms.send('You took long to verify. Aborting.')

        if cat.content == f'{ctx.prefix}abort':
            return await ctx.send('Aborting.')

        cat = cat.content.split('.')

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"https://graph.instagram.com/{cat[0]}?fields=id,username&access_token={cat[1]}") as response:
                    if response.status >= 400:  # usually bad id or token, less commonly network
                        return await dms.send('```That was unsuccessful.```')

                    info = await response.json()

                    query = """  users 
                               SET instagram_username = (?)
                               WHERE user_id = (?)
                            """

                    await self.bot.db.execute(query, (info['username'], ctx.author.id,))
                    await self.bot.db.commit()

                    await ctx.send("Verified Instagram in your server profile.")

        except IndexError:
            await dms.send('```Bad format. Make sure to copy the entire code.```')

    @profile.command()
    async def behance(self, ctx):
        """Verify your Behance account."""

        code = generate_code()

        await ctx.send(f'Please paste the following verification code anywhere in the About Me section of your '
                       f'Behance profile. When you are done, send your Behance username here.\n'
                       f'Your code: `{code}`')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            reply = await self.bot.wait_for('message', timeout=600.0, check=check)
            username = reply.content
        except TimeoutError:
            return await ctx.send('You took long to verify. Aborting.')

        if username == f'{ctx.prefix}abort':
            return await ctx.send('Aborting.')

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://www.behance.net/{username}') as response:
                html = await response.text()
                parsed = await self.bot.loop.run_in_executor(None, fetch, html)

                results = parsed.find('div', class_='UserInfo-bio-OZA')

                # Not sure about this errorhandler
                # Or wait until python 3.10 update to use AttributeError name?
                if results is None:
                    return await ctx.send("This Behance profile does not exist. Aborting.")

        bio = results.span.text

        if code in bio:

            query = """UPDATE users 
                       SET behance_username = (?)
                       WHERE user_id = (?)
                    """

            await self.bot.db.execute(query, (username, ctx.author.id,))
            await self.bot.db.commit()

            return await ctx.send("Verified Behance in your server profile.")
        else:
            return await ctx.send("Could not find the verification code in your Behance's About Me. Aborting.")


class Commissions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.message_cd = commands.CooldownMapping.from_cooldown(3, 10, commands.BucketType.member)  # 3 per 10 seconds
        self.image_cd = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)

    class RequestFlags(commands.FlagConverter, prefix='--', delimiter=' '):
        description: str
        budget: str
        method: str
        deadline: str
        contact: str

    class ReviewFlags(commands.FlagConverter, prefix='--', delimiter=' '):
        order: str
        artist: discord.Member
        comments: str
        stars: float

    @commands.Cog.listener('on_message')
    async def message_send(self, message):
        """General message reputation boost"""
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        if message.author.bot:
            return

        if message.guild is None:
            return

        bucket = self.message_cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            return

        id_rows = await self.bot.db.execute("""SELECT * FROM reputation_config 
                                               WHERE channel_id = ?""", (ctx.channel.id,))
        id_rows = await id_rows.fetchone()

        if id_rows is None:
            reputation_add = 1
        else:
            reputation_add = id_rows[1]

        await self.bot.db.execute(f"""INSERT INTO users (user_id, reputation, weekly_reputation)
                                    VALUES (?, ?, ?)
                                    ON CONFLICT(user_id)
                                    DO UPDATE SET reputation = reputation + excluded.reputation, 
                                    weekly_reputation = weekly_reputation+ + excluded.weekly_reputation""",
                                  (message.author.id, reputation_add, reputation_add,))
        await self.bot.db.commit()

    @commands.Cog.listener('on_message')
    async def picture_send(self, message):
        """Reputation bonus for pictures"""
        # Marked for rewriting

        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        if not message.attachments:
            return

        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.channel.id not in [constants.critique, constants.showcase, constants.testing]:
            return

        bucket = self.image_cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            return

        reputation_add = {constants.critique: 5,
                          constants.showcase: 15,
                          constants.testing: 50}

        await self.bot.db.execute(f"""INSERT INTO users (user_id, reputation, weekly_reputation)
                                    VALUES (?, ?, ?)
                                    ON CONFLICT(user_id)
                                    DO UPDATE SET reputation = reputation + excluded.reputation, 
                                    weekly_reputation = weekly_reputation+ + excluded.weekly_reputation""",
                                  (message.author.id, reputation_add[message.channel.id], reputation_add[message.channel.id],))
        await self.bot.db.commit()

    @commands.Cog.listener('on_message')
    async def message_bump(self, message):
        """Gives reputation for Disboard bumpers"""

        if message.interaction is None:
            return

        if message.interaction.name == 'bump':
            await self.bot.db.execute(f"""INSERT INTO users (user_id, reputation, weekly_reputation)
                                        VALUES (?, ?, ?)
                                        ON CONFLICT(user_id)
                                        DO UPDATE SET reputation = reputation + excluded.reputation, 
                                        weekly_reputation = weekly_reputation+ + excluded.weekly_reputation""",
                                      (message.interaction.user.id, 10, 10,))
            await self.bot.db.commit()

    @commands.command(aliases=['rr'])
    @commands.guild_only()
    @staff_only()
    async def removerequest(self, ctx, order_id):
        """Removes a commission request."""

        channel = self.bot.get_channel(constants.commissions_postings)
        message = await channel.fetch_message(order_id)
        await message.delete()

        await self.bot.db.execute("""DELETE FROM commissions WHERE order_id = (?)""", (order_id,))
        await self.bot.db.commit()

        await ctx.send(f'\N{OK HAND SIGN} Deleted order `{order_id}`.')

    @commands.command()
    async def request(self, ctx):
        """Interactively place an order for a request."""

        await ctx.send("Hello. Please fill out the details of your request by copying and pasting the format below. "
                       "Edit it, then send it here. \n"
                       "```"
                       "--budget $10 USD \n"
                       "--description Help! My cousin photobombed my graduation photo. I want to remove him and that's "
                       "where you come in. Fortunately he's in the far background so shouldn't be too complex. \n"
                       "--method Paypal or Google Pay. If you have a ko-fi page that's cool too. \n"
                       "--deadline By next week \n"
                       "--contact Discord DMs"
                       "```")

        def check(message):
            return ctx.author.id == message.author.id and ctx.channel.id == message.channel.id

        msg = await ctx.bot.wait_for("message", check=check, timeout=600.0)
        flags = await self.RequestFlags.convert(ctx, msg.content)

        embed = Embed.from_dict({'title': f"{ctx.author.display_name}'s editing request",
                                 'color': discord.Color.og_blurple().value,
                                 'description': f'{flags.description} - {ctx.author.mention}',
                                 'fields': [
                                     {'name': 'Budget',
                                      'value': f'{flags.budget}',
                                      'inline': True},
                                     {'name': 'Method',
                                      'value': f'{flags.method}\n',
                                      'inline': False},
                                     {'name': 'Deadline',
                                      'value': f'{flags.deadline}\n',
                                      'inline': False},
                                     {'name': 'Contact',
                                      'value': f'{flags.contact}\n',
                                      'inline': True}
                                 ],
                                 'footer': {'text': 'Photoshop Park is not responsible for supervising any '
                                                    'transactions made during a commission. '},
                                 })

        confirm = await ctx.prompt(
            f"Please check your request to ensure that it contains the correct information. "
            f"Do you want to finalise your order?",
            embed=embed
        )
        if not confirm:
            return await ctx.send("Aborting.")

        channel = self.bot.get_channel(constants.commissions_postings)

        order = await channel.send(embed=embed)
        embed.add_field(name='Order ID', value=f'`{order.id}`', inline=False)

        await order.edit(embed=embed)

        await self.bot.db.execute(f"""INSERT INTO commissions (buyer_id, order_id, url)
                                    VALUES (?, ?, ?)""", (ctx.author.id, order.id, order.jump_url,))
        await self.bot.db.commit()

    @commands.command()
    async def review(self, ctx):
        """Interactively review a commission order."""

        rows = await self.bot.db.execute("""SELECT * FROM commissions WHERE buyer_id = (?)""", (ctx.author.id,))
        rows = await rows.fetchall()

        if not rows:
            return await ctx.send("Sorry, you can't review anyone if you don't have any active commissions. Aborting.")

        await ctx.send("Hello! If you enjoyed your commission, consider leaving a review for the artist. "
                       "It will encourage them as well as help future customers! Please use the following format. "
                       "You can find your `order` number by checking the DM I sent to you previously. \n\n"
                       "--order 777231684202266644 \n"
                       f"--artist {self.bot.user.mention}\n"
                       "--comments Was very patient and understood exactly what I wanted, fast work too! "
                       "Did a great job, would recommend and commission them again. \n"
                       "--stars 5 \n")

        def check(message):
            return ctx.author.id == message.author.id and ctx.channel.id == message.channel.id

        msg = await ctx.bot.wait_for("message", check=check, timeout=600.0)
        flags = await self.ReviewFlags.convert(ctx, msg.content)

        if flags.artist == ctx.author:
            return await ctx.send("You cannot rate yourself. Aborting.")

        # Check for star values
        if flags.stars < 0 or flags.stars > 5:
            return await ctx.send("Star values must be a number between 0 and 5. Aborting.")

        # Check for invalid order ID
        buyer_order = await self.bot.db.execute("""SELECT * FROM commissions WHERE order_id = (?)""", (flags.order,))
        buyer_order = await buyer_order.fetchone()
        if buyer_order is None:
            return await ctx.send("You do not own this commission or it is invalid. Aborting.")
        if buyer_order[-1] == 1:
            return await ctx.send("This order has already been reviewed. Aborting.")

        embed = Embed.from_dict({'title': f"{ctx.author.display_name}'s review of {flags.artist.display_name}",
                                 'color': discord.Color.og_blurple().value,
                                 'description': f'{flags.comments} - {ctx.author.mention}',
                                 'fields': [
                                     {'name': 'Original',
                                      'value': f'[Jump!]({buyer_order[3]})',
                                      'inline': True},
                                     {'name': 'Artist',
                                      'value': f'{flags.artist.mention}',
                                      'inline': True},
                                     {'name': 'Stars',
                                      'value': f'{flags.stars}',
                                      'inline': True},
                                     {'name': 'Order ID',
                                      'value': f'`{flags.order}`',
                                      'inline': True}
                                 ],
                                 'footer': {'text': 'This review reflects the opinion of the buyer and not that of '
                                                    'Photoshop Park.'},
                                 })

        confirm = await ctx.prompt(
            f"This will mark the request as completed. Do you want to finalise your review?",
            embed=embed
        )
        if not confirm:
            return await ctx.send("Aborting.")

        channel = self.bot.get_channel(constants.commissions_reviews)
        await channel.send(embed=embed)

        # Edit the original order to mark as completed
        channel = self.bot.get_channel(constants.commissions_postings)
        message = await channel.fetch_message(flags.order)
        embed = message.embeds[0]
        embed.colour = constants.red
        embed.title = f"{embed.title} - REQUEST COMPLETED"
        await message.edit(embed=embed)

        reputation_add = flags.stars * 10

        await self.bot.db.execute(f"""UPDATE commissions 
                               SET (seller_id, comments, stars, completed) = (?, ?, ?, ?)
                               WHERE order_id = (?)""", (ctx.author.id, flags.comments, flags.stars, 1, flags.order))
        await self.bot.db.execute(f"""INSERT INTO users (user_id, reputation, weekly_reputation)
                                    VALUES (?, ?, ?)
                                    ON CONFLICT(user_id)
                                    DO UPDATE SET reputation = reputation + excluded.reputation, 
                                    weekly_reputation = weekly_reputation+ + excluded.weekly_reputation""",
                                  (message.interaction.user.id, reputation_add, reputation_add,))
        await self.bot.db.commit()

    # @commands.command(aliases=['shistory'])
    # @commands.guild_only()
    # async def sellhistory(self, ctx, member: discord.Member):


async def setup(bot):
    await bot.add_cog(Meta(bot))
    await bot.add_cog(Commissions(bot))
