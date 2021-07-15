import asyncio
from discord.ext import commands
from discord import Embed
import discord
from utils import constants


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # [INACTIVE] For editing the rule embed.
    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def change(self, ctx):
    #     rules = self.bot.get_channel(constants.rules)
    #     msg = await rules.fetch_message(791682685515857920)
    #
    #     rule = f"We expect all members of our community to adhere by our rules below. " \
    #            f"Please ensure that you understand what they mean. \n" \
    #            f"If you would like to report an incident or have questions concerning our rules, " \
    #            f"please message <@575252669443211264>. \n\n" \
    #            f"**Rule 1**\n{constants.rule1}\n" \
    #            f"**Rule 2**\n{constants.rule2}\n" \
    #            f"**Rule 3**\n{constants.rule3}\n" \
    #            f"**Rule 4**\n{constants.rule4}\n" \
    #            f"**Rule 5**\n{constants.rule5}\n" \
    #            f"**Rule 6**\n{constants.rule6}\n" \
    #            f"**Rule 7**\n{constants.rule7}\n"
    #
    #     print(rule)
    #
    #     embed = Embed(
    #         title=f"Photoshop Discord Rules",
    #         color=constants.blurple,
    #         description=rule)
    #
    #     embed.set_thumbnail(url="https://i.postimg.cc/hj4bVZwg/ISW-EAR.png")
    #
    #     await msg.edit(embed=embed)

    # @commands.command()
    # async def vo(self, ctx):
    #     rules = self.bot.get_channel(constants.events)
    #     msg = await rules.fetch_message(850134966934306826)
    #     await msg.add_reaction("<:blobFingerGuns:833076453050023987>")

    @commands.command()
    async def unpin(self, ctx):
        await ctx.message.pin()

        await asyncio.sleep(10)

        await ctx.message.unpin()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def promote(self, ctx, member: discord.Member):

        content = f"**We're very glad that you could join us as a new helper!\n**" \
                  f"We have all sorts of exciting things planned. For now, why not pop in " \
                  f"the <#{constants.helpers_chat}> and say hello?"

        embed = Embed(
            title=f"Welcome to the Photoshop helpers team!",
            color=constants.blurple,
            description=content)

        embed.set_thumbnail(url="https://media.giphy.com/media/QG2bT1r0cDC6I/giphy.gif")

        await member.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reject(self, ctx, member: discord.Member, *, reason):

        embed = Embed(
            title=f"Not quite a helper... yet?",
            color=constants.blurple,
            description=f"**We're glad that you took the time to apply, but we can't add you as a helper just yet.**\n"
                        f"{reason}")

        embed.set_thumbnail(url="https://i.pinimg.com/originals/8d/66/f0/8d66f0431f5cf4229750749c13b005af.gif")

        await member.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
