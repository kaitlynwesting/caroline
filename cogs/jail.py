from discord.ext import commands
from cogs.utils import constants
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb://cakeHeadChef:cakeHeadChef@buttercream-shard-00-00.ilbju.mongodb.net:27017,buttercream-shard-00-01."
    "ilbju.mongodb.net:27017,buttercream-shard-00-02.ilbju.mongodb.net:27017/Discord?"
    "ssl=true&replicaSet=atlas-65nepc-shard-0&authSource=admin&retryWrites=true&w=majority"
)

db = cluster["Discord"]
collection = db["Nickname Jail"]


class Jail(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            result = collection.find_one({'prisoner_id': before.id})

            if result is not None:

                if after.nick != result['prisoner_nickname']:
                    await after.edit(nick=before.nick)
                    await (self.bot.get_channel(constants.logs)).send(f"{before.mention} tried to escape "
                                                                      f"nickname jail!")


def setup(bot):
    bot.add_cog(Jail(bot))
