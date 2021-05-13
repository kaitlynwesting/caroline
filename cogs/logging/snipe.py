import discord
from discord.ext import commands
from utils import constants, embed_template


class Snipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_message_delete(self, message):
    #
    #     if message.author.id != constants.bot_id and message.author.id != constants.kat_id:
    #         deleted_log_channel = self.bot.get_channel(constants.deleted_message_log)
    #
    #         await embed_template.server_embed_full(
    #             deleted_log_channel,
    #             f"{message.author.avatar_url}",
    #             f"Message author: {message.author}",
    #             f'',
    #             f"Message deleted from: #{message.channel}:",
    #             f"{message.content}",
    #             f"Deleted message was sent",
    #             message.created_at,
    #             constants.blurple,
    #         )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.bot.snipes[message.channel.id] = message

    @commands.command(aliases=["deleted"])
    @commands.has_permissions(manage_messages=True)
    async def snipe(self,
                    ctx,
                    *,
                    channel: discord.TextChannel = None
                    ):

        channel = ctx.channel if channel is None else channel

        try:
            message = self.bot.snipes[channel.id]
        except KeyError:
            return await ctx.send("Nothing to snipe since most recent restart.")

        await embed_template.server_embed_full(
            ctx.channel,
            f"{message.author.avatar_url}",
            f"Message author: {message.author}",
            f'',
            f"Last message deleted from: #{message.channel}:",
            f"{message.content}",
            f"Deleted message was sent",
            message.created_at,
            constants.blurple,
        )


def setup(bot):
    bot.add_cog(Snipe(bot))
