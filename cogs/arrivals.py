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
            print(member)

            user_message = (
                f"**Now partnered with the [r/Photoshop](https://www.reddit.com/r/photoshop/) subreddit! ^_^** \n\n"
                f"Thank you for accepting our rules! "
                f"For reference, you can find them again in <#{constants.rules}>.\n\n"
                f"**Here's a fast rundown on what to do now, in the server:**\n",
                f"• Introduce yourself in the <#{constants.introduce_yourself} channel, if you'd like! We want to get ",
                f"to know all of our wonderful community members!\n\n",
                f"• Technical help with Photoshop is exchanged in our help channels: <#{constants.alpha}> + ",
                f"<#{constants.beta}>. We'll help you to the best of our ability.\n\n",
                f"• To receive advice and suggestions for your ongoing works in progress (WIPs), head over to",
                f"<#{constants.critique}> and post your work, or give advice to others.\n\n",
                f"• Improve your skills and make fantastic art by participating in the most recent event in our",
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
                text="We are always developing new features!"
            )

            await member.send(embed=embed)


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
