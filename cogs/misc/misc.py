from discord.ext import commands
from discord import Embed
from utils import constants


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # [INACTIVE] For editing the rule embed.
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def change(self, ctx):
        rules = self.bot.get_channel(constants.rules)
        msg = await rules.fetch_message(791682685515857920)

        rule = f"We expect all members of our community to adhere by our rules below. " \
               f"Please ensure that you understand what they mean. \n" \
               f"If you would like to report an incident or have questions concerning our rules, " \
               f"please message <@575252669443211264>. \n\n" \
               f"**Rule 1**\n{constants.rule1}\n" \
               f"**Rule 2**\n{constants.rule2}\n" \
               f"**Rule 3**\n{constants.rule3}\n" \
               f"**Rule 4**\n{constants.rule4}\n" \
               f"**Rule 5**\n{constants.rule5}\n" \
               f"**Rule 6**\n{constants.rule6}\n" \
               f"**Rule 7**\n{constants.rule7}\n"

        print(rule)

        embed = Embed(
            title=f"Photoshop Discord Rules",
            color=constants.blurple,
            description=rule)

        embed.set_thumbnail(url="https://i.postimg.cc/hj4bVZwg/ISW-EAR.png")

        await msg.edit(embed=embed)

    # @commands.command()
    # async def vo(self, ctx):
    #     rules = self.bot.get_channel(constants.events)
    #     msg = await rules.fetch_message(850134966934306826)
    #     await msg.add_reaction("<:blobFingerGuns:833076453050023987>")

def setup(bot):
    bot.add_cog(Misc(bot))
