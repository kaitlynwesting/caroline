import asyncio
import discord
import time
from aiosqlite import OperationalError, IntegrityError
from discord.ext import commands
from cogs.utils import constants
from cogs.utils.views import PaginationView
from cogs.utils.decorators import staff_only, mod_only


async def get_embed_list(data_list):
    embed_list = [discord.Embed.from_dict({'title': f'{data[0]}',
                                           'description': f'{data[1]}',
                                           'image': {'url': f'{data[2]}'},
                                           'footer': {'text': f'Badge {i + 1} out of {len(data_list)}'},
                                           'color': constants.medal_colours[data[-1]],
                                           }) for i, data in enumerate(data_list)]

    return embed_list


class BadgesMeta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["badges", "achievements"])
    @commands.guild_only()
    async def badge(self, ctx, member: discord.Member = None):
        """
        Preview the badges you own, or preview the badges owned by someone else.

        :param ctx: commands.Context
        :param member: discord.Member
        :return: None
        """
        if member is None:
            member = ctx.author

        id_rows = await self.bot.db.execute("""SELECT * FROM badges_users 
                                              WHERE user_id = ?""", (member.id,))
        id_rows = await id_rows.fetchall()

        if not id_rows:
            await ctx.send("You have no badges. Wait, how is that even possible?")
            return

        id_rows = tuple([item[1] for item in id_rows])

        question_placeholders = ','.join(['?'] * len(id_rows))

        data_list = await self.bot.db.execute(f"""SELECT * FROM badges_master
                                            WHERE badge_id IN ({question_placeholders})""", id_rows, )
        data_list = await data_list.fetchall()

        embed_list = await get_embed_list(data_list)
        await PaginationView(embed_list=embed_list, ctx=ctx).start(ctx=ctx, notification_context=ctx)

    @badge.command()
    @commands.guild_only()
    @staff_only()
    async def all(self, ctx):
        """
        Preview all currently available badges.

        :param ctx: commands.Context
        :return: None
        """
        rows = await self.bot.db.execute("""SELECT * FROM badges_master 
                                            ORDER BY position ASC""")
        rows = await rows.fetchall()

        embed_list = await get_embed_list(rows)
        await PaginationView(embed_list=embed_list, ctx=ctx).start(ctx=ctx, notification_context=ctx)

    @badge.command(aliases=["award, bestow", "giveth"])
    @commands.guild_only()
    @mod_only()
    async def give(self, ctx, badge_id: int, member: discord.Member = None, give_mode=None):
        """
        Manually give a badge to yourself, or to someone else.
        Do not pass an argument to the give_mode parameter!

        :param ctx: commands.Context
        :param badge_id: int
        :param member: discord.Member
        :param give_mode: Any
        :return:
        """
        if member is None:
            member = ctx.author

        if member.bot:
            return

        rows = await(
            await self.bot.db.execute("""SELECT * FROM badges_users 
                                        WHERE user_id = (?) AND badge_id = (?)""", (member.id, badge_id))).fetchall()

        if rows != [] and give_mode is None:
            return await ctx.send(f"{member.display_name} already has this badge.")
        elif rows:
            return

        await self.bot.db.execute("""INSERT INTO badges_users (user_id, badge_id, date_earned)
                                    VALUES (?, ?, ?)
                                    ON CONFLICT(user_id, badge_id)
                                    DO NOTHING""", (member.id, badge_id, time.time()))

        rows = await(
            await self.bot.db.execute("""SELECT * FROM badges_master 
                                        WHERE badge_id = (?)""", (badge_id,))).fetchall()

        await self.bot.db.commit()

        embed = discord.Embed.from_dict({'title': f'A wild present appeared!',
                                         'fields': [
                                             {'inline': True,
                                              'name': 'You\'ve received a present from Photoshop Discord!',
                                              'value': f'The gift box, coated in grey matte paper and neatly '
                                                       f'secured with blue ribbon, gave no indication of what '
                                                       f'might reside inside. It glows faintly as you pick it up. \n'
                                                       f'A huge red bowtie knot adorns the lid of '
                                                       f'the box, waiting to be unravelled.'}
                                         ],
                                         'thumbnail': {'url': 'https://media.discordapp.net/attachments/'
                                                              '819766454035152896/877218700363706378/'
                                                              'IREALLYSWEAR2.png?width=540&height=676'},
                                         'footer': {'text': 'React with 🤏 to this message within the next 60s '
                                                            'to pull the ribbon on the box.'},
                                         'color': constants.blurple
                                         })

        dms = await member.create_dm()

        await dms.send(embed=embed)

        def check(reaction, user):
            return str(reaction.emoji) == '🤏'

        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await dms.send('Well, you missed the present elves. Not to worry, though, you can still check presents '
                           'with `!badges`.')
            return

        embed_list = await get_embed_list(rows)
        await PaginationView(embed_list=embed_list, ctx=ctx).start(ctx=ctx, notification_context=dms)

    @badge.command(aliases=["gb", "massgive", "mg"])
    @commands.guild_only()
    @mod_only()
    async def givebatch(self, ctx, member: discord.Member, *, badge_ids: str):
        """
        Manually give a badge to yourself, or to someone else.
        Do not pass an argument to the give_mode parameter!

        :param ctx: commands.Context
        :param member: discord.Member
        :param badge_ids: str
        :return:
        """
        if member.bot:
            return

        badge_ids = badge_ids.split()
        data_list = []

        for badge_id in badge_ids:
            data_item = (member.id, badge_id, time.time())
            data_list.append(data_item)

        await self.bot.db.executemany("""INSERT INTO badges_users (user_id, badge_id, date_earned)
                                        VALUES (?, ?, ?)
                                        ON CONFLICT(user_id, badge_id)
                                        DO NOTHING""", data_list)
        #
        # rows = await(
        #     await self.bot.db.execute("""SELECT * FROM badges_master
        #                                 WHERE badge_id = (?)""", (badge_id,))).fetchall()

        # await self.bot.db.commit()
        #
        # dms = await member.create_dm()
        #
        # await dms.send(embed=embed)
        #
        # def check(reaction, user):
        #     return str(reaction.emoji) == '🤏'
        #
        # try:
        #     await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        # except asyncio.TimeoutError:
        #     await dms.send('Well, you missed the present elves. Not to worry, though, you can still check presents '
        #                    'with `!badges`.')
        #     return
        #
        # embed_list = await get_embed_list(rows)
        # await PaginationView(embed_list=embed_list, ctx=ctx).start(ctx=dms)

    @give.error
    async def on_error(self, ctx, error):
        ctx.error_handled = True

        # Safely unwrap the CommandInvokeError
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        # Bad inputs errors
        if isinstance(error, discord.errors.Forbidden):
            pass

        # Bad inputs errors
        if isinstance(error, IntegrityError):
            pass

        # Usually a locked database error
        elif isinstance(error, OperationalError):
            pass
        else:
            ctx.error_handled = False


class BadgesFilters(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def stone_age(self, ctx):
    #     for member in ctx.guild.members:
    #         closed_date = datetime(2021, 3, 31, 14, 0, 42)
    #
    #         if member.joined_at <= closed_date:
    #             print(f"{member.name}, known as {member.display_name} who joined at {member.joined_at}")
    #             await BadgesMeta.give(self, ctx, 1, member)

    @commands.Cog.listener('on_message')
    async def messages_sent(self, message):

        # if message.author.id not in constants.early_testers:
        #     return

        if message.author.bot:
            return

        if message.guild is None:
            return

        await self.bot.db.execute("""INSERT INTO badges_users_stats (user_id, messages_sent, wants_notifications)
                                    VALUES (?, ?, ?)
                                    ON CONFLICT(user_id)
                                    DO UPDATE SET messages_sent = messages_sent + 1""", (int(message.author.id), 1, 1,))

        messages_sent_qty = (await(
            await self.bot.db.execute("""SELECT messages_sent FROM badges_users_stats
                                        WHERE user_id = (?)""", (message.author.id,))).fetchone())[0]

        series_list = (await(
            await self.bot.db.execute("""SELECT * FROM badges_master
                                        WHERE series = (?)""", ('m',))).fetchall())[::-1]

        for count, row in enumerate(series_list):
            if int(messages_sent_qty) >= int(row[6]):
                ctx = await self.bot.get_context(message)
                await BadgesMeta.give(self, ctx, int(row[4]), message.author, 0)
                # row[6] and row[4] are the thresholds and the ids respectively

        await self.bot.db.commit()

    @commands.Cog.listener('on_message')
    async def artworks_sent(self, message):

        # if message.author.id not in constants.early_testers:
        #     return

        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.channel.id not in [constants.testing, constants.events, constants.showcase]:
            return

        if not message.attachments:
            return

        def get_filetype(filename: str):
            return (str(filename)).split('.')[-1]

        if set(map(get_filetype, message.attachments)).issubset(constants.allowed_filetypes) is False:
            return

        await self.bot.db.execute("""INSERT INTO badges_users_stats (user_id, artworks_sent)
                                    VALUES (?, ?)
                                    ON CONFLICT(user_id)
                                    DO UPDATE SET artworks_sent = artworks_sent + 1""", (message.author.id, 1,))

        await self.bot.db.commit()

        artworks_sent_qty = (await(
            await self.bot.db.execute("""SELECT artworks_sent FROM badges_users_stats
                                        WHERE user_id = (?)""", (message.author.id,))).fetchone())[0]

        series_list = (await(
            await self.bot.db.execute("""SELECT * FROM badges_master
                                        WHERE series = (?)""", ('p',))).fetchall())[::-1]

        for count, row in enumerate(series_list):
            if artworks_sent_qty >= row[6]:
                ctx = await self.bot.get_context(message)
                await BadgesMeta.give(self, ctx, int(row[4]), message.author, 0)

    @commands.Cog.listener('on_message')
    async def welcomes_sent(self, message):

        # if message.author.id not in constants.early_testers:
        #     return

        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.channel.id not in [constants.introduce_yourself, constants.lobby]:
            return

        content = message.content.lower()
        content = content.replace('welkom', 'welcome')

        if 'welcome' not in content:
            return

        if not any(i in content for i in constants.welcome_keywords):
            if not content.startswith('welcome'):
                return

        await self.bot.db.execute("""INSERT INTO badges_users_stats (user_id, welcomes_sent)
                                    VALUES (?, ?)
                                    ON CONFLICT(user_id)
                                    DO UPDATE SET welcomes_sent = welcomes_sent + 1""", (message.author.id, 1,))

        await self.bot.db.commit()

        welcomes_sent_qty = (await(
            await self.bot.db.execute("""SELECT welcomes_sent FROM badges_users_stats
                                        WHERE user_id = (?)""", (message.author.id,))).fetchone())[0]

        series_list = (await(
            await self.bot.db.execute("""SELECT * FROM badges_master
                                        WHERE series = (?)""", ('w',))).fetchall())[::-1]

        for count, row in enumerate(series_list):
            if welcomes_sent_qty >= row[6]:
                ctx = await self.bot.get_context(message)
                await BadgesMeta.give(self, ctx, int(row[4]), message.author, 0)

    @commands.Cog.listener('on_member_remove')
    async def delete_leaves(self, member):
        """
        Delete user info rows when a member leaves the server.

        :param member:
        :return:
        """

        await self.bot.db.execute("""DELETE FROM badges_users
                                            WHERE user_id = (?)""", (int(member.id),))

        await self.bot.db.execute("""DELETE FROM badges_users_stats
                                    WHERE user_id = (?)""", (int(member.id),))

        await self.bot.db.execute("""DELETE FROM event_votes
                                    WHERE user_id = (?)""", (int(member.id),))

        await self.bot.db.commit()


async def setup(bot):
    await bot.add_cog(BadgesMeta(bot))
    await bot.add_cog(BadgesFilters(bot))
