import asyncio, traceback

from cogs.utils import constants, decorators, formats

from datetime import datetime, timedelta

import discord
from discord.ext import commands, menus

async def get_embed_list(data_list):
    embed_list = [discord.Embed.from_dict({'title': f'Seasonal Leaderboard - Season {data[0][-1]}',
                                           'description': f'{description}',
                                           'footer': {'text': f'Page {menu.current_page + 1} out of '
                                                              f'{self.get_max_pages()}'},
                                           'color': constants.blurple
                                           }) for i, data in enumerate(data_list)]

    return embed_list


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.season_number = bot.season_number

    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def votes(self, ctx, member: discord.Member = None, season: int = None):
        """
        Check your event votes, or someone else's votes.
        """

        if member is None:
            member = ctx.author

        if member.bot:
            return await ctx.send("I am a bot, what did you expect?")

        if season is None:
            season = self.season_number

        votes_qty = (await(
            await self.bot.db.execute("""SELECT votes FROM event_votes
                                        WHERE user_id = (?) AND season_number = (?)""",
                                      (member.id, season))).fetchone())[0]

        if not votes_qty:
            await ctx.send(f"{member.display_name} hasn't participated in Season {season} events yet. No points!")
            return

        await ctx.send(f"For **Season {season}**, {member.display_name} has "
                       f"collected {votes_qty} vote{formats.plural(votes_qty)}.")

    @votes.command(aliases=['top', 'rank'])
    @commands.guild_only()
    async def leaderboard(self, ctx, season: int = None):
        """
        Check the leaderboard of the current season.

        :param ctx: commands.Context
        :param season: int
        :return:
        """

        if season is None:
            season = self.season_number

        ranking_info = await(
            await self.bot.db.execute("""SELECT user_id, votes, season_number FROM event_votes
                                        WHERE season_number = (?)
                                        ORDER BY votes DESC""", (season,))).fetchall()

        prev = None
        rank = 0
        incr = 1
        positions_data = []

        for user_id, value, season_number in ranking_info:
            if value != prev:
                rank += incr
                incr = 1
            else:
                incr += 1
            positions_data.append((rank, user_id, value, season))
            prev = value

        embed_list = await get_embed_list(positions_data)


    @votes.command()
    @commands.guild_only()
    @decorators.mod_only()
    async def set(self, ctx, member: discord.Member, season: int, new_votes: int):
        """
        Manually set a member's season event votes.

        :param ctx: commands.Context
        :param member: discord.Member
        :param season: int
        :param new_votes: int
        :return:
        """

        if member.bot:
            return await ctx.send("I am a bot, what did you expect?")

        old_votes = (await(
            await self.bot.db.execute("""SELECT votes FROM event_votes
                                         WHERE user_id = (?) AND season_number = (?)""",
                                      (member.id, season))).fetchone())

        if old_votes is None:
            old_votes = 0
        else:
            old_votes = old_votes[0]

        embed = discord.Embed.from_dict({'title': 'Confirmation',
                                         'description': f'You are about to update the event vote count for '
                                                        f'{member.display_name} in Season {season}.',
                                         'fields': [
                                             {'inline': True,
                                              'name': 'New value',
                                              'value': f'{new_votes}'},
                                             {'inline': True,
                                              'name': 'Old value',
                                              'value': f'{old_votes}'}
                                         ],
                                         'footer': {'text': 'React with 👍 to this message within the next 60s '
                                                            'to confirm.'},
                                         'color': constants.blurple
                                         })
        await ctx.send(embed=embed)

        def check(reaction, user):
            return str(reaction.emoji) == '👍' and user == ctx.author

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Cancelled because of timeout.')
        else:
            # Upsert update votes
            await self.bot.db.execute("""INSERT INTO event_votes
                                        VALUES (?, ?, ?)
                                        ON CONFLICT(user_id, season_number)
                                        DO UPDATE SET votes = (?)""", (member.id, season, new_votes, new_votes,))

            await self.bot.db.commit()

            await ctx.send('Update successful.')

    @leaderboard.error
    async def on_error(self, ctx, error):
        ctx.error_handled = True

        # Safely unwrap the CommandInvokeError
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        # Out of bounds
        if isinstance(error, IndexError):
            embed = discord.Embed.from_dict({'title': f'Oups! IndexError with !{ctx.command}',
                                             'fields': [
                                                 {'inline': True,
                                                  'name': 'Bad number',
                                                  'value': f'Make sure to pick a valid season number. '
                                                           f'The latest season available is {self.bot.season_number}'
                                                           f'```py\n{type(error).__name__}: {error}```'}
                                             ],
                                             'footer': {'text': 'React with 👍 to this message within the next 60s '
                                                                'to confirm.'},
                                             'color': constants.blurple
                                             })
            await ctx.send(embed=embed)
            var = traceback.format_exc()
            await ctx.send(var[:2000])
        else:
            ctx.error_handled = False


class EventVetting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vote_emoji = '⭐'

    @commands.Cog.listener('on_message')
    async def submission_vetting(self, message):
        ctx = await self.bot.get_context(message)

        def role_to_id(role):
            return role.id

        if ctx.guild is None:
            return

        if ctx.channel.id not in [constants.events, constants.testing]:
            return

        if ctx.author.bot:
            return

        if '[BEFORE]' in ctx.message.content:
            return

        if (
                "Challenge Number" in str(message.content) and
                any(r in map(role_to_id, message.author.roles) for r in constants.staff_roles) is True
        ):
            return

        if (
                message.attachments == [] and
                any(r in map(role_to_id, message.author.roles) for r in constants.staff_roles) is True
        ):
            return

        if (
                any(r in map(role_to_id, message.author.roles) for r in constants.staff_roles) is False and
                message.attachments == []
        ):
            await message.delete()
            reminder = await message.channel.send(
                f"Hi, {message.author.mention}! This channel is for finished submissions only. "
                f"If you have questions or would like feedback, ask in the <#{constants.lobby}>."
            )
            await reminder.delete(delay=5.0)
            return

        # If all other checks have passed, this indicates a genuine submission
        await ctx.message.add_reaction(self.vote_emoji)

        # Upsert member votes
        await self.bot.db.execute("""INSERT INTO event_votes
                                    VALUES (?, ?, ?)
                                    ON CONFLICT(user_id, season_number)
                                    DO UPDATE SET votes = votes + 1""",
                                  (ctx.author.id, self.bot.season_number, 1,))

        await self.bot.db.commit()

    @commands.Cog.listener('on_raw_reaction_add')
    async def vote_add(self, payload):

        if payload.guild_id is None:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        context_emoji = str(payload.emoji)
        voted_times = 0
        ctx = await self.bot.get_context(message)

        if payload.member.bot:
            return

        if ctx.author.bot:
            return

        if ctx.channel.id not in [constants.events, constants.testing]:
            return

        if datetime.now() - ctx.message.created_at > timedelta(days=8):
            return

        if '[BEFORE]' in ctx.message.content:
            return

        if '[SOURCE]' in ctx.message.content:
            return

        if context_emoji != self.vote_emoji:
            return

        async for message in ctx.channel.history(limit=30):
            if 'Challenge Number' in message.content:

                # Looks at each reaction for each submission after event marker
                async for submission in ctx.channel.history(after=message):

                    for reaction in submission.reactions:

                        async for user in reaction.users():

                            if user.bot:
                                pass

                            if user == payload.member and str(reaction) == self.vote_emoji:

                                voted_times += 1

                                if voted_times > 1:
                                    await ctx.message.remove_reaction(reaction, user)
                                    reminder_message = await ctx.channel.send(f"**No voting more than once, "
                                                                              f"{user.mention}!** If you wish to "
                                                                              f"vote for a different person, remove "
                                                                              f"your previous vote first.")
                                    await reminder_message.delete(delay=5.0)
                                    return

                            # So they didn't vote twice. Maybe they voted for themselves, though
                            if user == ctx.author and user == submission.author:
                                await ctx.message.remove_reaction(reaction, user)
                                reminder_message = await ctx.send(f"**Shame, {user.mention}, you tried to vote "
                                                                  f"for yourself!** Self voting is not allowed.")
                                await reminder_message.delete(delay=5.0)

                                return

                await self.bot.db.execute("""INSERT INTO event_votes
                                            VALUES (?, ?, ?)
                                            ON CONFLICT(user_id, season_number)
                                            DO UPDATE SET votes = votes + 1""",
                                          (ctx.author.id, self.bot.season_number, 1,))

                await self.bot.db.commit()
                return

    @commands.Cog.listener('on_raw_reaction_remove')
    async def vote_removal(self, payload):

        if payload.guild_id is None:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        context_emoji = str(payload.emoji)
        ctx = await self.bot.get_context(message)

        if ctx.channel.id not in [constants.events, constants.testing]:
            return

        if datetime.now() - ctx.message.created_at > timedelta(days=8):
            return

        if context_emoji != self.vote_emoji:
            return

        await self.bot.db.execute("""UPDATE event_votes
                                     SET votes = votes - 1
                                     WHERE user_id = (?) AND season_number = (?)""",
                                  (ctx.author.id, self.bot.season_number,))

        await self.bot.db.commit()
        return

    @commands.Cog.listener('on_raw_message_delete')
    async def submission_deletion(self, payload):

        if payload.guild_id is None:
            return

        if payload.cached_message is None:
            return

        if payload.cached_message.author.bot:
            return

        if not payload.cached_message.reactions:
            return

        for react in payload.cached_message.reactions:
            if react.emoji == '⭐':
                await self.bot.db.execute("""UPDATE event_votes
                                             SET votes = votes - (?)
                                             WHERE user_id = (?) AND season_number = (?)""",
                                          (react.count, payload.cached_message.author.id, self.bot.season_number,))

            await self.bot.db.commit()
            return


def setup(bot):
    bot.add_cog(Events(bot))
    bot.add_cog(EventVetting(bot))
