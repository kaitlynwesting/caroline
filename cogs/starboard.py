from discord.ext import commands
from discord import Embed

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

        for react in context_message.reactions:
            if react.emoji == '⭐' and react.count >= constants.star_min:

                # Is it a new star message?

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

                    # Get message data

                    star_message = await starboard.fetch_message(result['star_id'])
                    await star_message.edit(content=f"**⭐{react.count}** from <#{react.message.channel.id}> | "
                                                    f"ID: {react.message.id}")

                    # Add star to message db

                    return

    @commands.Cog.listener('on_reaction_remove')
    async def star_remover(self, reaction, user):

        if reaction.message.guild is None:
            return

        for react in reaction.message.reactions:
            if react.emoji == '⭐':
                
                # Check if message is in starboard

                if result_count > 0:
                    # Get current star ammount
                    
                    if star_ammount > constants.star_min:
                        # Remove message
                        pass
                
                    # Remove star
                    pass
                
                return


def setup(bot):
    bot.add_cog(Starboard(bot))
