import discord
from discord.ext import commands
from discord.utils import get


class Welcome(commands.Cog):

    # Constructor
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.pending != after.pending:

            member = await self.bot.fetch_user(before.id)
            print(member)

            user_message = (
                f"Thank you for accepting our rules! "
                f"For reference, you can find them again in <#777237462904209429>.\n\n"
                f"**Here's a fast rundown on what we do in this server:**\n",
                f"• Technical help with using Photoshop is exchanged in our help channels. If you have a question,",
                f"simply find a non-busy help channel, read the embed on asking good questions, and ask! A community ",
                f"member or helper will usually come to take a look. Please remember that we are all volunteers!\n\n",
                f"• To receive advice and suggestions for your ongoing works in progress (WIPs), head over to",
                f"<#818878248670068766> and post your art.\n\n",
                f"• Improve your skills and make fantastic art by participating in the most recent event in our",
                f"<#778410460185493505> channel!\n\n"
                f"We wish you an enjoyable and excellent stay. See you inside, and let's learn together!"
            )

            embed = discord.Embed(
                title=f'Welcome to Photoshop Discord, {member.name}!',
                color=0x349feb,
                description=' '.join(user_message)
            )

            embed.set_thumbnail(url="https://i.postimg.cc/L6wQ6HNq/5e78affab2547d678e4c5458dd931381.gif")

            embed.set_footer(
                text="This bot was written for Photoshop Discord by Kat. We are always developing new features!"
            )

            await member.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))
