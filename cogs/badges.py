import discord
import time
from aiosqlite import OperationalError, IntegrityError
from datetime import datetime
from discord.ext import commands, menus
from utils import constants
from utils.decorators import staff_only, mod_only
from utils.embed_template import error_embed


class MyMenu(menus.MenuPages):

    @menus.button('🔢', position=menus.First(-1))
    async def stop(self, payload):
        await self.stop()


class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, data):
        embed = discord.Embed(
            title=data[0],
            description=data[1]
        )
        embed.set_image(url=data[2])
        embed.set_footer(text=f'Page {menu.current_page + 1} out of {self.get_max_pages()}')

        return embed


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

        data = await self.bot.db.execute(f"""SELECT * FROM badges_master
                                            WHERE badge_id IN ({question_placeholders})""", id_rows, )
        data = await data.fetchall()
        print(data)

        menu = menus.MenuPages(source=EmbedPageSource(data, per_page=1),
                               timeout=60.0,
                               clear_reactions_after=True)

        await menu.start(ctx)

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

        menu = menus.MenuPages(source=EmbedPageSource(rows, per_page=1),
                               timeout=60.0,
                               clear_reactions_after=True)

        await menu.start(ctx)

    @badge.command(aliases=["award, bestow", "giveth"])
    @commands.guild_only()
    @mod_only()
    async def give(self, ctx, badge_id: int, member: discord.Member = None):
        """
        Manually give a badge to yourself, or to someone else.

        :param ctx: commands.Context
        :param badge_id: int
        :param member: discord.Member
        :return:
        """
        if member is None:
            member = ctx.author

        if member.bot:
            return

        rows = await(
            await self.bot.db.execute("""SELECT * FROM badges_users 
                                        WHERE user_id = (?) AND badge_id = (?)""", (member.id, badge_id))).fetchall()

        if rows:
            return

        await self.bot.db.execute("""INSERT INTO badges_users (user_id, badge_id, date_earned)
                                    VALUES (?, ?, ?)
                                    ON CONFLICT(user_id, badge_id)
                                    DO NOTHING""", (member.id, badge_id, time.time()))

        rows = await(
            await self.bot.db.execute("""SELECT * FROM badges_master 
                                        WHERE badge_id = (?)""", (badge_id,))).fetchall()

        await self.bot.db.commit()

        menu = menus.MenuPages(source=EmbedPageSource(rows, per_page=1),
                               timeout=60.0,
                               clear_reactions_after=True)

        dms = await member.create_dm()

        await dms.send("Congratulations!")
        
        await menu.start(ctx, channel=dms)

    @give.error
    async def on_error(self, ctx, error):
        ctx.error_handled = True

        # Safely unwrap the CommandInvokeError
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        # Bad inputs errors
        if isinstance(error, discord.errors.Forbidden):
            await error_embed(ctx,
                              f"Oups! 403 Forbidden",
                              f"I tried to send a badge to you, but you had your DMs off.",
                              f"```py\n{type(error).__name__}: {error}```",
                              f'',
                              constants.yellow)

        # Bad inputs errors
        if isinstance(error, IntegrityError):
            await error_embed(ctx,
                              f"Oups! IntegrityError with !{ctx.command}",
                              f"Bad input, not that serious",
                              f"```py\n{type(error).__name__}: {error}```",
                              f'',
                              constants.yellow)

        # Usually a locked database error
        elif isinstance(error, OperationalError):
            await error_embed(ctx,
                              f"Oups! OperationalError with !{ctx.command}",
                              f"This is BAF and will directly affect anything to do with storing data",
                              f"```py\n{type(error).__name__}: {error}```",
                              f'An automated error report has been submitted... possibly',
                              constants.red)
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

        if message.author.id not in constants.early_testers:
            return

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
                await BadgesMeta.give(self, ctx, int(row[4]), message.author)
                # row[6] and row[4] are the thresholds and the ids respectively

        await self.bot.db.commit()

    @commands.Cog.listener('on_message')
    async def artworks_sent(self, message):

        if message.author.id not in constants.early_testers:
            return

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
                await BadgesMeta.give(self, ctx, int(row[4]), message.author)

    @commands.Cog.listener('on_message')
    async def welcomes_sent(self, message):

        if message.author.id not in constants.early_testers:
            return

        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.channel.id not in [constants.testing, constants.introduce_yourself, constants.lobby]:
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
                await BadgesMeta.give(self, ctx, int(row[4]), message.author)

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


def setup(bot):
    bot.add_cog(BadgesMeta(bot))
    bot.add_cog(BadgesFilters(bot))
