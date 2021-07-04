import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from utils import constants


# COG FOR NEW ARRIVALS AND DEPARTS

class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.pending != after.pending:

            member = await self.bot.fetch_user(before.id)

            user_message = (
                f"**Now partnered with the [r/Photoshop](https://www.reddit.com/r/photoshop/) subreddit! ^_^** \n\n"
                f"Thank you for accepting our <#{constants.rules}>!\n\n"
                f"**Here's a fast rundown on what to do now, in the server:**\n",
                f"• Introduce yourself in the <#{constants.introduce_yourself} channel, if you'd like! We want to get ",
                f"to know all of our wonderful community members!\n\n",
                f"• User help with Photoshop is exchanged in our help channels: <#{constants.alpha}> + ",
                f"<#{constants.beta}>. We'll be happy to lend a hand, provided you ask a good question "
                f"(send `!tag help` to me to know how).\n\n",
                f"• Improve your skills and make fresh art by participating in the most recent challenge in our",
                f"<#{constants.events}> channel, which changes weekly :)\n\n"
                f"That's it for now! We wish you an enjoyable and excellent stay. See you inside!"
            )

            embed = discord.Embed(
                title=f'Welcome to Photoshop Discord, {member.name}!',
                color=constants.blurple,
                description=' '.join(user_message)
            )

            embed.set_thumbnail(url="https://i.postimg.cc/L6wQ6HNq/5e78affab2547d678e4c5458dd931381.gif")

            embed.set_footer(
                text="We love Photoshop!"
            )

            await member.send(embed=embed)

            await asyncio.sleep(180)

            user_message = (
                f"**How very silly of me!** \n\n"
                f"I was instructed to tell you this: \n"
                f"• If you'd like to stay tuned on important updates and features from the Photoshop server, "
                f"you can subscribe to announcements by doing `!sub announcements` in <#{constants.bot_commands}>. \n"
                f"• If you'd like to get notified each week for our new weekly events, you can subscribe, similarly, "
                f"by doing `!sub events` in <#{constants.bot_commands}>. (The events are fun, I promise!) \n\n"
                f"Okay, that's all, for real this time."
            )

            embed = discord.Embed(
                title=f'I forgot to tell you something!',
                color=constants.blurple,
                description=' '.join(user_message)
            )

            embed.set_thumbnail(url="https://i.pinimg.com/originals/e4/43/4c/e4434c1d99dd02a12daef6fcf05be9d9.gif")

class Joins(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = get(member.guild.text_channels, name="logs")
        await channel.send(f"{member.mention} has joined us.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = get(member.guild.text_channels, name="logs")
        await channel.send(f"{member.mention} has left.")


def setup(bot):
    bot.add_cog(Welcome(bot))
    bot.add_cog(Joins(bot))
