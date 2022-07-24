import discord
from discord.ext import commands
from cogs.utils import constants, checks
from cogs.utils.views import PaginationView


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_embed_list(self, data_list):
        descriptions = []

        for num, entry in enumerate(data_list):
            server = self.bot.get_guild(constants.server_id)
            member = server.get_member(entry[1])
            descriptions.append(f"**{entry[0]}**. {member.mention} - {entry[2]} votes\n")

        descriptions = [descriptions[x:x + 5] for x in range(0, len(descriptions), 5)]
        embed_list = [discord.Embed.from_dict({'title': f'Seasonal Leaderboard - Season 2',
                                               'description': f"{''.join(descriptions[i])}",
                                               'footer': {'text': f'Badge {i + 1} out of {len(descriptions)}'},
                                               'color': constants.blurple
                                               }) for i, data in enumerate(descriptions)]

        return embed_list

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
            season = self.bot.season_number

        votes_qty = (await(
            await self.bot.db.execute("""SELECT votes FROM event_votes
                                        WHERE user_id = (?) AND season_number = (?)""",
                                      (member.id, season))).fetchone())[0]

        if not votes_qty:
            return await ctx.send(f"{member.display_name} hasn't participated in Season {season} events yet.")

        await ctx.send(f"For **Season {season}**, {member.display_name} has "
                       f"collected {votes_qty} votes.")

    @votes.command(aliases=['top', 'rank'], hidden=True)
    @commands.guild_only()
    async def leaderboard(self, ctx, season: int = None):
        """
        Check the leaderboard of the current season.
        """

        if season is None:
            season = self.bot.season_number

        ranking_info = await(
            await self.bot.db.execute("""SELECT * FROM event_votes
                                        WHERE season_number = (?)
                                        ORDER BY votes DESC""", (season,))).fetchall()

        prev = None
        rank = 0
        incr = 1
        positions_data = []

        for user_id, season_number, votes in ranking_info:
            if votes != prev:
                rank += incr
                incr = 1
            else:
                incr += 1
            positions_data.append((rank, user_id, votes, season))
            prev = votes

        embed_list = await self.get_embed_list(positions_data)
        await PaginationView(embed_list=embed_list, ctx=ctx).start(ctx=ctx, notification_context=ctx)

    @votes.command()
    @commands.guild_only()
    @checks.mod_only()
    async def set(self, ctx, member: discord.Member, season: int, new_votes: int):
        """
        Manually set a member's season event votes.
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

        confirm = await ctx.prompt(
            f"{member.display_name} in Season {season} will be {new_votes} instead of {old_votes}. Are you sure?"
        )
        if not confirm:
            return await ctx.send("Aborting.")

        await self.bot.db.execute("""INSERT INTO event_votes
                                    VALUES (?, ?, ?)
                                    ON CONFLICT(user_id, season_number)
                                    DO UPDATE SET votes = (?)""", (member.id, season, new_votes, new_votes,))

        await self.bot.db.commit()

        await ctx.send('Update successful.')


class EventVetting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vote_emoji = '\N{WHITE MEDIUM STAR}'

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
            reminder = await message.channel.send(
                f"Hi, {message.author.mention}! This channel is for finished submissions only. "
                f"If you have questions or would like feedback, ask in the <#{constants.lobby}>."
            )
            await reminder.delete(delay=30.0)
            await message.delete()
            return

        # If all other checks have passed, this indicates a genuine submission
        await ctx.message.add_reaction(self.vote_emoji)

        # Update reputation
        await self.bot.db.execute(f"""INSERT INTO users (user_id, reputation, weekly_reputation)
                                    VALUES (?, ?, ?)
                                    ON CONFLICT(user_id)
                                    DO UPDATE SET reputation = reputation + excluded.reputation, 
                                    weekly_reputation = weekly_reputation + excluded.weekly_reputation""",
                                  (ctx.author.id, 50, 50))

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

        if ctx.author.bot:
            return

        if ctx.channel.id not in [constants.events, constants.testing]:
            return

        if '[BEFORE]' in ctx.message.content:
            return

        if '[SOURCE]' in ctx.message.content:
            return

        if context_emoji != self.vote_emoji:
            return

        async for message in ctx.channel.history(limit=30):
            if 'Challenge Number' not in message.content:
                continue

            # Looks at each reaction for each submission after event marker
            async for submission in ctx.channel.history(after=message):

                for reaction in submission.reactions:

                    async for user in reaction.users():
                        print(user)

                        if user.bot:
                            continue

                        if user == payload.member and str(reaction) == self.vote_emoji:

                            voted_times += 1

                            if voted_times > 1:
                                await ctx.message.remove_reaction(reaction, user)
                                reminder_message = await ctx.channel.send(f"**No voting more than once, "
                                                                          f"{user.mention}!** If you wish to "
                                                                          f"vote for a different person, remove "
                                                                          f"your previous vote first.")
                                await reminder_message.delete(delay=30.0)
                                return

                        # So they didn't vote twice. Maybe they voted for themselves, though
                        if user == ctx.author and user == submission.author:
                            await ctx.message.remove_reaction(reaction, user)
                            reminder_message = await ctx.send(f"**Shame, {user.mention}, you tried to vote "
                                                              f"for yourself!** Self voting is not allowed.")
                            return await reminder_message.delete(delay=5.0)

            # If all checks have passed
            await self.bot.db.execute("""INSERT INTO event_votes
                                        VALUES (?, ?, ?)
                                        ON CONFLICT(user_id, season_number)
                                        DO UPDATE SET votes = votes + 1""",
                                      (ctx.author.id, self.bot.season_number, 1,))

            await self.bot.db.commit()
            return

    @commands.Cog.listener('on_raw_reaction_remove')
    async def vote_deletion(self, payload):

        if payload.guild_id is None:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        context_emoji = str(payload.emoji)
        ctx = await self.bot.get_context(message)

        if context_emoji != self.vote_emoji:
            return

        await self.bot.db.execute("""UPDATE event_votes
                                     SET votes = votes - 1
                                     WHERE user_id = (?) AND season_number = (?)""",
                                  (message.author.id, self.bot.season_number,))

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

        # Update reputation
        await self.bot.db.execute(f"""INSERT INTO users (user_id, reputation, weekly_reputation)
                                        VALUES (?, ?, ?)
                                        ON CONFLICT(user_id)
                                        DO UPDATE SET reputation = reputation - excluded.reputation, 
                                        weekly_reputation = weekly_reputation - excluded.weekly_reputation""",
                                  (payload.cached_message.author.id, 50, 50))

        for react in payload.cached_message.reactions:
            if react.emoji == '\N{WHITE MEDIUM STAR}':
                await self.bot.db.execute("""UPDATE event_votes
                                             SET votes = votes - (?)
                                             WHERE user_id = (?) AND season_number = (?)""",
                                          (react.count, payload.cached_message.author.id, self.bot.season_number,))

            await self.bot.db.commit()
            return


async def setup(bot):
    await bot.add_cog(Events(bot))
    await bot.add_cog(EventVetting(bot))
