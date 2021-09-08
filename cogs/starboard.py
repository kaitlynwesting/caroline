from discord.ext import commands
from discord import Embed
from pymongo import MongoClient
from cogs.utils import constants


class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_raw_reaction_add')
    async def star_listener(self, payload):
        context_channel = self.bot.get_channel(payload.channel_id)
        context_message = await context_channel.fetch_message(payload.message_id)
        context_emoji = str(payload.emoji)

        if context_channel.guild is None:
            return

        star_result = collection.find_one({"_id": 1})
        star_min = 5

        for react in context_message.reactions:
            if react.emoji == '⭐' and react.count >= star_min:

                # It is time to document the votes
                result_count = collection.count_documents({"_id": int(react.message.id)})

                starboard = self.bot.get_channel(constants.starboard)

                if result_count == 0:
                    embed = Embed(
                        description=f"{context_message.content}",
                        timestamp=context_message.created_at,
                        color=constants.blurple
                    )

                    embed.set_author(name=context_message.author.display_name,
                                     icon_url=context_message.author.avatar_url)
                    embed.add_field(name="Original",
                                    value=f"[Jump!]({context_message.jump_url})")

                    if react.message.attachments:  # if there are attachments
                        embed.set_image(url=context_message.attachments[0])

                    star_message = await starboard.send(f"**⭐{react.count}** from <#{context_message.channel.id}> | "
                                                        f"ID: {context_message.id}",
                                                        embed=embed)
                    post = {
                        f"_id": int(react.message.id),
                        f"channel_id": int(react.message.channel.id),
                        f"star_id": int(star_message.id),
                        f"stars": int(react.count)
                    }

                    collection.insert_one(post)

                    return
                else:

                    result = collection.find_one({'_id': context_message.id})

                    star_message = await starboard.fetch_message(result['star_id'])
                    await star_message.edit(content=f"**⭐{react.count}** from <#{react.message.channel.id}> | "
                                                    f"ID: {react.message.id}")

                    collection.update_one(
                        {"_id": react.message.id},
                        {"$set": {f"stars": int(react.count)}},
                        upsert=True
                    )

                    return

    @commands.Cog.listener('on_reaction_remove')
    async def star_remover(self, reaction, user):

        if reaction.message.guild is None:
            return

        for react in reaction.message.reactions:
            if react.emoji == '⭐':

                result_count = collection.count_documents({"_id": int(react.message.id)})

                starboard = self.bot.get_channel(constants.starboard)

                if result_count != 0:

                    result = collection.find_one({'_id': reaction.message.id})
                    star_result = collection.find_one({"_id": 1})
                    star_min = int(star_result["value"])

                    star_message = await starboard.fetch_message(result['star_id'])
                    await star_message.edit(content=f"**⭐{react.count}** from <#{reaction.message.channel.id}> | "
                                                    f"ID: {reaction.message.id}")

                    collection.update_one(
                        {"_id": reaction.message.id},
                        {"$set": {f"stars": int(react.count)}},
                        upsert=True
                    )

                    return


def setup(bot):
    bot.add_cog(Starboard(bot))
