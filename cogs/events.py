import discord
from discord.ext import commands
from datetime import datetime, timedelta
from cogs.utils import constants, formats


# async def get_embed_list(data_list):
#     embed_list = [discord.Embed.from_dict({'title': f'Seasonal Leaderboard - Season {data[0][-1]}',
#                                            'description': f'{description}',
#                                            'footer': {'text': f'Page {menu.current_page + 1} out of '
#                                                               f'{self.get_max_pages()}'},
#                                            'color': constants.blurple
#                                            }) for i, data in enumerate(data_list)]
#
#     return embed_list


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vote_emoji = '⭐'
        # self.season_number = bot.season_number
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 604800, commands.BucketType.member)

    @commands.Cog.listener('on_message')
    async def submission_vetting(self, message):
        ctx = await self.bot.get_context(message)

        if ctx.author.bot:
            return

        if ctx.guild is None:
            return

        if ctx.channel.id not in [constants.events, constants.testing]:
            return

        def role_to_id(role):
            return role.id

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
            reminder = await message.channel.send(
                f"{message.author.mention}, this channel is for finished submissions only. "
                f"If you have questions or would like feedback, please ask in the <#{constants.lobby}>."
            )
            await message.delete(delay=10.0)
            await reminder.delete(delay=10.0)
            return

        # If all other checks have passed, this indicates a genuine submission

        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await message.channel.send("You are being rate limited.")
        else:
            await message.channel.send("Added VOTES!")
            await ctx.message.add_reaction(self.vote_emoji)

        # Upsert member votes - handle this elsewhere
        # await self.bot.db.execute("""INSERT INTO event_votes
        #                                 VALUES (?, ?, ?)
        #                                 ON CONFLICT(user_id, season_number)
        #                                 DO UPDATE SET votes = votes + 1""",
        #                           (ctx.author.id, self.bot.season_number, 1,))

        # await self.bot.db.commit()

    @commands.Cog.listener('on_raw_reaction_add')
    async def vote_add(self, payload):

        if payload.member.bot:
            return

        if payload.guild_id is None:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        context_emoji = str(payload.emoji)
        voted_times = 0
        ctx = await self.bot.get_context(message)

        if ctx.author.bot:
            return

        if ctx.channel.id not in [constants.events, constants.testing]:
            return

        if datetime.now() - ctx.message.created_at > timedelta(days=8):
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

        if payload.cached_message is None:
            return

        if payload.cached_message.author.bot:
            return

        if payload.guild_id is None:
            return

        if not payload.cached_message.reactions:
            return

        # for react in payload.cached_message.reactions:
        #     if react.emoji == '⭐':
        #         await self.bot.db.execute("""UPDATE event_votes
        #                                          SET votes = votes - (?)
        #                                          WHERE user_id = (?) AND season_number = (?)""",
        #                                   (react.count, payload.cached_message.author.id, self.bot.season_number,))
        #
        #     await self.bot.db.commit()

    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def votes(self, ctx, member: discord.Member = None, season: int = None):
        """Check your event votes, or someone else's votes."""

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

    # @votes.command(aliases=['top', 'rank'])
    # @commands.guild_only()
    # async def leaderboard(self, ctx, season: int = None):
    #     """
    #     Check the leaderboard of the current season.
    #
    #     :param ctx: commands.Context
    #     :param season: int
    #     :return:
    #     """
    #
    #     if season is None:
    #         season = self.season_number
    #
    #     ranking_info = await(
    #         await self.bot.db.execute("""SELECT user_id, votes, season_number FROM event_votes
    #                                     WHERE season_number = (?)
    #                                     ORDER BY votes DESC""", (season,))).fetchall()
    #
    #     prev = None
    #     rank = 0
    #     incr = 1
    #     positions_data = []
    #
    #     for user_id, value, season_number in ranking_info:
    #         if value != prev:
    #             rank += incr
    #             incr = 1
    #         else:
    #             incr += 1
    #         positions_data.append((rank, user_id, value, season))
    #         prev = value
    #
    #     embed_list = await get_embed_list(positions_data)


async def setup(bot):
    await bot.add_cog(Events(bot))
