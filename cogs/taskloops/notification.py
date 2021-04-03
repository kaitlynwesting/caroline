import asyncio
import discord
from discord.ext import tasks, commands
from discord.utils import get
from datetime import datetime, timezone, timedelta
import pytz

import traceback
import sys
import random


class Notification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.help_dormant.start()

    # LOOP TO CHECK FOR DORMANT HELP CHANNELS
    @tasks.loop(seconds=60)
    async def help_dormant(self):
        channelList = [780519472444080158,
                       777207889277616192]  # hardcoded two help channels, unfortunately can't get channel by names, doesn't support it

        for channel in channelList:
            channel = self.bot.get_channel(channel)

            async for message in channel.history(limit=1):
                if message.author == self.bot.user:
                    pass
                else:
                    nowTime = datetime.now(tz=timezone.utc)
                    messageTime = pytz.utc.localize(message.created_at)
                    duration = nowTime - messageTime
                    threshold = timedelta(hours=1)  # how long before channel marked as inactive?

                    if duration >= threshold:
                        print("Hmm...")
                        embed = discord.Embed(
                            color=0x349feb
                        )

                        embed.set_author(name=f"Open help channel", icon_url="https://i.postimg.cc/BZMpHQQV/image5.jpg")

                        embed.add_field(
                            name=f"Some tips to keep in mind before you ask:",
                            value=f"""• Refrain from asking generic or vague questions, such as "Can I get help" or "Why isn't this working".
• Explain what you're trying to do, what you have tried, and the outcome. This greatly facilitates the work of any potential helpers.
• Include a screenshot or snip of your Photoshop workspace, if appropriate.""",
                            inline=False)
                        embed.set_footer(text="Others will try to help you solve the problem, if they can. Sit tight!")

                        await message.channel.send(embed=embed)
                    else:
                        pass

    # CLOSE HELP CHANNEL MANUALLY
    @commands.command()
    async def close(self, ctx):
        channelList = [780519472444080158, 777207889277616192]

        if ctx.channel.id in channelList:
            embed = discord.Embed(
                color=0x349feb
            )

            embed.set_author(name=f"Open help channel", icon_url="https://i.postimg.cc/BZMpHQQV/image5.jpg")

            embed.add_field(
                name=f"Some tips to keep in mind before you ask:",
                value=f"""• Refrain from asking generic or vague questions, such as "Can I get help" or "Why isn't this working".
• Explain what you're trying to do, what you have tried, and the outcome. This greatly facilitates the work of any potential helpers.
• Include a screenshot or snip of your Photoshop workspace, if appropriate.""",
                inline=False)
            embed.set_footer(text="Others will try to help you solve the problem, if they can. Sit tight!")

            await ctx.send(embed=embed)

        else:
            await ctx.send("Please use that in the proper channels, i.e. our help channels.")


    # CHECC PING
    @commands.command()
    async def ping(self, ctx):

        await ctx.send(f"Pong! The latency is {round(self.bot.latency, 3)} milliseconds.")


def setup(bot):
    bot.add_cog(Notification(bot))
