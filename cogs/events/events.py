import discord
from discord.ext import commands
from datetime import datetime, timedelta
from pymongo import MongoClient
from utils import constants, helpers

cluster = MongoClient(
    "mongodb://cakeHeadChef:cakeHeadChef@buttercream-shard-00-00.ilbju.mongodb.net:27017,buttercream-shard-00-01."
    "ilbju.mongodb.net:27017,buttercream-shard-00-02.ilbju.mongodb.net:27017/Discord?"
    "ssl=true&replicaSet=atlas-65nepc-shard-0&authSource=admin&retryWrites=true&w=majority"
)

db = cluster["Discord"]
collection = db["Seasons"]

season_result = collection.find_one({"_id": 1})
season_number = int(season_result["season"])


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def votes(self, ctx, participant: discord.Member = None):
        if participant is None:
            participant = ctx.author

        print(participant.display_name)
        result_count = collection.count_documents({"_id": int(participant.id)})

        if result_count == 0:
            await ctx.send(f"I couldn't find {participant.display_name}'s profile. "
                           "This is probably because they've never participated in any of our seasons, and "
                           "so have received no votes!")
            return

        result = collection.find_one({"_id": int(participant.id)})
        await ctx.send(f"For **Season {season_number}**, {participant.display_name} has "
                       f"collected {result[f'season_{season_number}']} "
                       f"vote{helpers.plural(result[f'season_{season_number}'])}.")


class EventVetting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def submission_vetting(self, message):

        def role_to_id(role):
            return role.id

        if message.guild is None:
            return

        if message.channel.id != constants.events:
            return

        if message.author == self.bot.user:
            return

        if (
                "Challenge Number" in str(message.content) and
                any(r in map(role_to_id, message.author.roles) for r in constants.mod_roles) is True
        ):
            return

        if (
                any(r in map(role_to_id, message.author.roles) for r in constants.mod_roles) is False and
                message.attachments == []
        ):
            await message.delete()
            reminder = await message.channel.send(
                f"Hi, {message.author.mention}! This channel is for finished submissions only. "
                f"If you have questions or would like feedback, ask in the <#{constants.lobby}>."
            )
            await reminder.delete(delay=3)

            return

        # If all other checks have passed, this indicates a genuine submission, and should be given a vote
        await message.add_reaction("<:blobFingerGuns:833076453050023987>")

        # It is time to document the votes
        result_count = collection.count_documents({"_id": int(message.author.id)})

        # If no such user has been found, create a new document for them
        if result_count == 0:
            post = {
                f"_id": message.author.id,
                f"season_{season_number}": 1,
            }

            collection.insert_one(post)
            return

        # If this user already exists, update the season field with +1 point
        result = collection.find_one({"_id": message.author.id})
        collection.update_one(
            {"_id": message.author.id},
            {"$set": {f"season_{season_number}": int(result[f"season_{season_number}"]) + 1}},
            upsert=True
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.guild_id is None:
            return

        context_channel = self.bot.get_channel(payload.channel_id)
        context_message = await context_channel.fetch_message(payload.message_id)
        context_emoji = str(payload.emoji)
        voting_emoji = "<:blobFingerGuns:833076453050023987>"
        voted_times = 0

        # Auto voting score updating is already done in the above method.
        if payload.member == self.bot.user:
            return

        if context_channel.id != constants.events:
            return

        if datetime.now() - context_message.created_at > timedelta(days=8):
            return

        if context_emoji == voting_emoji:
            async for message in context_channel.history(limit=25):
                if 'Challenge Number' in message.content:
                    async for submission in context_channel.history(after=message):
                        # Looks at each reaction for each submission after event marker
                        for reaction in submission.reactions:
                            # Looks at each user for each reaction
                            async for user in reaction.users():

                                if user == payload.member and str(reaction) == voting_emoji:

                                    voted_times += 1

                                    if voted_times > 1:
                                        await context_message.remove_reaction(reaction, user)
                                        reminder_message = \
                                            await context_channel.send(f"**No voting more than once, "
                                                                       f"{user.mention}!** If you wish to "
                                                                       f"vote for a different person, remove your "
                                                                       f"previous vote first.")
                                        await reminder_message.delete(delay=3)

                                        result = collection.find_one({"_id": int(context_message.author.id)})
                                        collection.update_one(
                                            {"_id": int(context_message.author.id)},
                                            {"$set": {f"season_{season_number}": int(
                                                result[f"season_{season_number}"]) + 1}},
                                            upsert=True
                                        )

                                        return

                                # So they didn't vote twice. Maybe they voted for themselves, though
                                if user == payload.member and user == submission.author:
                                    await context_message.remove_reaction(reaction, user)
                                    reminder_message = \
                                        await context_channel.send(f"**Shame, {user.mention}, you tried to vote"
                                                                   f"for yourself!** Self voting is not allowed.")
                                    await reminder_message.delete(delay=3)

                                    result = collection.find_one({"_id": int(context_message.author.id)})
                                    collection.update_one(
                                        {"_id": int(context_message.author.id)},
                                        {"$set": {
                                            f"season_{season_number}": int(result[f"season_{season_number}"]) + 1}},
                                        upsert=True
                                    )

                                    return

                    result = collection.find_one({"_id": int(context_message.author.id)})
                    collection.update_one(
                        {"_id": int(context_message.author.id)},
                        {"$set": {f"season_{season_number}": int(result[f"season_{season_number}"]) + 1}},
                        upsert=True
                    )
                    return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        context_channel = self.bot.get_channel(payload.channel_id)
        context_message = await context_channel.fetch_message(payload.message_id)
        context_emoji = str(payload.emoji)
        voting_emoji = "<:blobFingerGuns:833076453050023987>"

        if context_channel.id != constants.events:
            return

        if datetime.now() - context_message.created_at > timedelta(days=8):
            return

        if context_emoji != voting_emoji:
            return

        result = collection.find_one({"_id": int(context_message.author.id)})
        collection.update_one(
            {"_id": int(context_message.author.id)},
            {"$set": {f"season_{season_number}": int(result[f"season_{season_number}"]) - 1}},
            upsert=True
        )
        return


    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #
    #     context_channel = self.bot.get_channel(payload.channel_id)
    #     context_message = await context_channel.fetch_message(payload.message_id)
    #     context_emoji = str(payload.emoji)
    #
    #     voting_emoji = "<:blobFingerGuns:833076453050023987>"
    #     voted_times = 0
    #
    #     if context_channel.id != constants.events:
    #         return
    #
    #     if context_emoji != voting_emoji:
    #         return
    #
    #     if context_message.author == self.bot.user:
    #         return
    #
    #     async for message in context_channel.history(limit=10):
    #
    #         if 'Challenge Number' in message.content:
    #
    #             async for submission in context_channel.history(after=message):
    #
    #                 for reaction in submission.reactions:
    #
    #                     async for user in reaction.users():
    #                         print(user, reaction)
    #                         if user == payload.member and str(reaction) == voting_emoji:
    #
    #                             voted_times += 1
    #
    #                             if voted_times > 1:
    #                                 await context_message.remove_reaction(reaction, user)
    #                                 reminder_message = \
    #                                     await context_channel.send(f"**No voting more than once, "
    #                                                                f"{user.mention}!** If you wish to "
    #                                                                f"vote for a different person, remove your "
    #                                                                f"previous vote first.")
    #                                 await reminder_message.delete(delay=3)
    #
    #                                 return
    #
    #                         if user == payload.member and user == submission.author:
    #                             await context_message.remove_reaction(reaction, user)
    #                             reminder_message = \
    #                                 await context_channel.send(f"**Shame, {user.mention}, you tried to vote "
    #                                                            f"for yourself!** Self voting is not allowed.")
    #                             await reminder_message.delete(delay=3)
    #
    #                             return
    #
    #     result = collection.find_one({"_id": int(context_message.author.id)})
    #     collection.update_one(
    #         {"_id": int(context_message.author.id)},
    #         {"$set": {f"season_{season_number}": int(result[f"season_{season_number}"]) + 1}},
    #         upsert=True
    #     )


def setup(bot):
    bot.add_cog(Events(bot))
    bot.add_cog(EventVetting(bot))
