import asyncpraw as ap
import requests
import pytz

from datetime import datetime, timedelta
from discord.ext import tasks, commands

from utils import constants


class RedditLoop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reddit.start()

    @tasks.loop(seconds=60)
    async def reddit(self):

        channel = self.bot.get_channel(constants.reddit)

        async for message in channel.history(limit=2):
            message_time = pytz.utc.localize(message.created_at)
            time_now = datetime.now(pytz.utc)
            time_difference = time_now - message_time

            if time_difference < timedelta(hours=24):
                return

            if str(message.type) != 'MessageType.pins_add':
                await message.add_reaction('🔢')
                await message.unpin()

                reddit = ap.Reddit(
                    client_id='-EXpNodmhibB5Q',
                    client_secret='GXd8P6XRCavNalat37J1--5uVBIz_Q',
                    user_agent='Mozilla/5.0',
                )

                subreddit = await reddit.subreddit("Photoshop")
                top_posts = subreddit.top("day", limit=5)
                content = ''

                async for post in top_posts:

                    if post.selftext.strip() == "":
                        description = ''
                    else:
                        description = f"{post.selftext[0:600]}...\n"

                    activity = f"`{post.score} upvotes | {post.num_comments} comments | u/{post.author}` \n\n"

                    content = content + (f"**[{post.title}]({post.shortlink})**\n{description}{activity}")

                url = "https://discord.com/api/webhooks/818239712153042954/fo1a3onL-nS1ZE93nBSqPBytThPSNM8hU14VUzy_qenMdEoPEUNex2pHaJ6JLPu2jtzj"

                embed = {
                    "title": "Top posts today from r/Photoshop:",
                    "description": f"{content}",
                    "color": constants.blurple,
                }

                data = {
                    "embeds": [
                        embed
                    ],
                }

                result = requests.post(url, json=data)
                if 200 <= result.status_code < 300:
                    print(f"Webhook sent with {result.status_code} code")
                else:
                    print(f"Not sent with {result.status_code} code, response:\n{result.json()}")

                await reddit.close()

                async for message in channel.history(limit=1):
                    await message.pin()
                    await message.publish()


def setup(bot):
    bot.add_cog(RedditLoop(bot))
