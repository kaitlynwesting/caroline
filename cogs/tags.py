from datetime import datetime, timezone

import discord
from discord.ext import commands
from discord.utils import get

import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb://cakeHeadChef:cakeHeadChef@buttercream-shard-00-00.ilbju.mongodb.net:27017,buttercream-shard-00-01.ilbju.mongodb.net:27017,buttercream-shard-00-02.ilbju.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-65nepc-shard-0&authSource=admin&retryWrites=true&w=majority")
db = cluster["Discord"]
collection = db["Tags"]

max_document = max(list(collection.find()), key=lambda x:x['_id'])
max_id = int(max_document["_id"])

class Tags(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # Fetching tag command.
    @commands.command()
    async def tag(self, ctx, *, tagname):

        tagname = tagname.lower()
        collection.find({"name": tagname})
        result_count = collection.count_documents({"name": tagname})
        
        if result_count > 0:
            results = collection.find({"name": tagname})
            for result in results:
                await ctx.send(result["content"])
        else:
            await ctx.send("Sorry, no tag by that name...")
    
    # Adding tag command.
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def addtag(self, ctx, tagname):

        await ctx.send("Tagname set! Send your tag content below.")

        # This checks that the bot only responds to the author in the right channel
        def check(message):
                return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

        content = await self.bot.wait_for('message', check=check)
        
        if content.content.lower() is not "cancel":
            post = {
            "_id": max_id + 1, 
            "name": tagname,
            "author_id": ctx.author.id,
            "content": content.content,
            "created_at": datetime.now().astimezone(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S"),
            "uses": 0
            }

            collection.insert_one(post)

            await ctx.send("Your tag has been successfully inserted into the system. Congratulations!")
        else:
            await ctx.send("New tag has been cancelled.")
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def updatetag(self, ctx, *, tagname):

        await ctx.send("Tag ready for changing! Send your updated tag content below.")

        # This checks that the bot only responds to the author in the right channel
        def check(message):
                return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id
    
        content = await self.bot.wait_for('message', check=check)

        collection.update_one(
        {"name" : tagname},
        {"$set":
            {"content": content.content}
        }, upsert=True
        )

        await ctx.send("Your tag has been successfully updated!")
        #collection.insert_many([post1, post2])
        #collection.delete_one({"name": "Kat"})
        #collection.delete_many([post3, post4])

def setup(bot):
    bot.add_cog(Tags(bot))
