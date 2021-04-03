from discord.ext import commands
from utils import constants, embed_template


class Rules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # TOGGLE RULES FOR DUMMIES
    @commands.command(aliases=["rule"])
    async def rules(
            self,
            ctx,
            rule_number=0
    ):

        rule_text = getattr(constants, f"rule{rule_number}")

        await embed_template.server_embed(
            ctx.channel,
            f"Photoshop Discord Rules",
            f"**Rule {rule_number}**:\n"
            f"{rule_text}",
            f"",
            constants.blurple
        )

    @rules.error
    async def bounds_error(self, ctx, error):

        await ctx.send(
            f"Rules range from 1-7. \n"
            f"`{error}`"
        )


def setup(bot):
    bot.add_cog(Rules(bot))
