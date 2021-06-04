from discord.ext import commands
from pymongo import MongoClient
from utils import constants, numbers

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
    async def votes(self, ctx):
        result_count = collection.count_documents({"_id": int(ctx.author.id)})

        if result_count == 0:
            await ctx.send("Well, I couldn't find your profile. "
                           "This is probably because you've never participated in any of our seasons, and "
                           "so have received no votes!")
            return

        result = collection.find_one({"_id": int(ctx.author.id)})
        await ctx.send(f"For **Season {season_number}**, you have collected {result[f'season_{season_number}']} "
                       f"vote{numbers.plural(result[f'season_{season_number}'])}.")


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

        if (
                message.attachments == [] and
                any(r in map(role_to_id, message.author.roles) for r in constants.mod_roles) is True or
                message.author == self.bot.user
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

        context_channel = self.bot.get_channel(payload.channel_id)
        context_message = await context_channel.fetch_message(payload.message_id)
        context_emoji = str(payload.emoji)

        voting_emoji = "<:blobFingerGuns:833076453050023987>"
        voted_times = 0

        if context_channel.id != constants.testing:
            return

        if context_emoji != voting_emoji:
            return

        if context_message.author == self.bot.user:
            return

        async for message in context_channel.history(limit=20):

            if 'Challenge Number' in message.content:

                async for submission in context_channel.history(after=message):

                    for reaction in submission.reactions:

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

                                    return

                                result = collection.find_one({"_id": context_message.author.id})
                                collection.update_one(
                                    {"_id": message.author.id},
                                    {"$set": {f"season_{season_number}": int(result[f"season_{season_number}"]) + 1}},
                                    upsert=True
                                )

                            if user == payload.member and user == submission.author:
                                await context_message.remove_reaction(reaction, user)
                                reminder_message = \
                                    await context_channel.send(f"**Shame, {user.mention}, you tried to vote "
                                                               f"for yourself!** Self voting is not allowed.")
                                await reminder_message.delete(delay=3)

                                return


def setup(bot):
    bot.add_cog(Events(bot))
    bot.add_cog(EventVetting(bot))
