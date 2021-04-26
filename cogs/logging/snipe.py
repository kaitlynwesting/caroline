from discord.ext import commands
from datetime import datetime
from utils import constants, embed_template


class Snipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if message.author.id != constants.bot_id and message.author.id != constants.kat_id:

            deleted_log_channel = self.bot.get_channel(constants.deleted_message_log)

            await embed_template.server_embed_full(
                deleted_log_channel,
                f"{message.author.avatar_url}",
                f"Message author: {message.author}",
                f"Message deleted from: #{message.channel}:",
                f"{message.content}",
                f"Deleted message was sent",
                message.created_at,
                constants.blurple,
            )


def setup(bot):
    bot.add_cog(Snipe(bot))
