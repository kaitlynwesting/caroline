from datetime import datetime, timezone
from discord.ext import commands
from utils import constants

from pymongo import MongoClient

cluster = MongoClient(
    "mongodb://cakeHeadChef:cakeHeadChef@buttercream-shard-00-00.ilbju.mongodb.net:27017,buttercream-shard-00-01."
    "ilbju.mongodb.net:27017,buttercream-shard-00-02.ilbju.mongodb.net:27017/Discord?"
    "ssl=true&replicaSet=atlas-65nepc-shard-0&authSource=admin&retryWrites=true&w=majority"
)

db = cluster["Discord"]
collection = db["Tags"]


class Tags(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Fetching tag command.
    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tag_name):
        """
        Fetches tags from a database.

        :param ctx:
        :param tag_name: str
        :return:
        """

        tag_name = tag_name.lower()
        collection.find({"name": tag_name})
        result_count = collection.count_documents({"name": tag_name})

        if result_count > 0:
            results = collection.find({"name": tag_name})
            for result in results:
                await ctx.send(result["content"])

                collection.update_one(
                    {"name": tag_name},
                    {"$set":
                         {"uses": result["uses"] + 1}
                     }, upsert=True
                )
        else:
            await ctx.send("Couldn't find a tag by that name. Sorry.")

    # Adding tag command.
    @tag.command()
    @commands.guild_only()
    @commands.check_any(commands.has_role(constants.helper), commands.has_permissions(kick_members=True))
    async def create(self, ctx, *, tag_name):
        """
        Creates and stores new tags in a database.

        :param ctx:
        :param tag_name:
        :return:
        """
        tags_dictionary = list(collection.find())
        max_id = 0
        for d in tags_dictionary:
            if int(str(d['_id'])) > max_id:
                max_id = d['_id']

        await ctx.send("Tag name set! Send your tag content below. Send `cancel` to cancel.")

        # This checks that the bot only responds to the author in the right channel
        def check(message):
            return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

        content = await self.bot.wait_for('message', check=check)

        if content.content.lower() != "cancel":
            post = {
                "_id": max_id + 1,
                "name": tag_name,
                "author_id": ctx.author.id,
                "content": content.content,
                "created_at": datetime.now().astimezone(timezone.utc).strftime("%B %d, %Y at %H:%M:%S"),
                "uses": 0
            }

            collection.insert_one(post)

            await ctx.send("Your tag has been successfully inserted into the system. Congratulations!")
        else:
            await ctx.send("New tag has been cancelled.")

    @tag.command()
    @commands.guild_only()
    @commands.check_any(commands.has_role(constants.helper), commands.has_permissions(kick_members=True))
    async def edit(self,
                   ctx,
                   *,
                   tag_name):

        tag_query = collection.find_one({"name": tag_name})

        if ctx.author.id == tag_query['author_id'] or ctx.author.id == constants.kat_id:
            await ctx.send("Tag ready for changing! Send your updated tag content below.")

            # This checks that the bot only responds to the author in the right channel
            def check(message):
                return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

            content = await self.bot.wait_for('message', check=check)

            collection.update_one(
                {"name": tag_name},
                {"$set":
                     {"content": content.content}
                 }, upsert=True
            )

            await ctx.send("Your tag has been successfully updated!")
        else:
            await ctx.send("You do not own this tag.")
        # collection.insert_many([post1, post2])
        # collection.delete_one({"name": "Kat"})
        # collection.delete_many([post3, post4])


def setup(bot):
    bot.add_cog(Tags(bot))
