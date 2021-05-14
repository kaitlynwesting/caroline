from discord.ext import commands

from utils import constants, embed_template
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb://cakeHeadChef:cakeHeadChef@buttercream-shard-00-00.ilbju.mongodb.net:27017,buttercream-shard-00-01."
    "ilbju.mongodb.net:27017,buttercream-shard-00-02.ilbju.mongodb.net:27017/Discord?"
    "ssl=true&replicaSet=atlas-65nepc-shard-0&authSource=admin&retryWrites=true&w=majority"
)

db = cluster["Discord"]
collection = db["Nickname Jail"]


async def unanimalise(
        ctx,
        pardoned_member,
):
    if collection.find_one({'prisoner_id': pardoned_member.id}) is not None:
        pass
    else:
        await ctx.send(f"{pardoned_member} is not in nickname jail.")
        return

    collection.delete_one({'prisoner_id': pardoned_member.id})

    try:
        await embed_template.dm_manual_embed(
            pardoned_member,
            f"Released from Nickname Jail",
            f"You have been released from Nickname Jail, and are able to change your nickname again. Ensure that it is "
            f"something appropriate.",
            f"",
            constants.blurple
        )

        await ctx.channel.send(f"👌")

    except Exception as e:
        await ctx.channel.send(f"Tried to release {pardoned_member.mention} from nickname jail just now but failed. "
                               f"Error: `{e}`")
