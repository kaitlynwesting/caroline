from discord.ext import commands
from discord import Embed
import discord
from cogs.utils import constants


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
    # async def p(self, ctx):
    #     # rule = f"Fervent lover of Photoshop? Enjoy helping other users? We invite you to take the helper form " \
    #     #        f"[here](https://forms.gle/oXydP3mb5AYhHF6t5)! We hope to see you on the team!"
    # #
    #     embed = Embed(
    #         title=f"Exchanging help efficiently",
    #         color=constants.blurple
    #         )
    #
    #     embed.add_field(name=f"When requesting help:",
    #                     value=f"• Ask your question or explain your problem clearly in the help channels. Help will "
    #                           f" not given outside of the server.\n"
    #                           f"• Include images such as references or a workspace screenshot, if applicable. The "
    #                           f"better explained, the better we will be able to help you.\n"
    #                           f"• Be ready to learn proactively, if you are a new user. ",
    #                     inline=False)
    #
    #     embed.add_field(name=f"When giving help:",
    #                     value=f"• Guide the mentee in the correct direction, but do not spoonfeed them. \n"
    #                           f" Instruct the mentee on the best approaches to take, and features to learn. "
    #                           f"Do not simply send them the `.psd` or finished image. \n"
    #                           f"• Encourage new users of Photoshop to develop their knowledge by pointing them to "
    #                           f"useful resources, such as the Adobe Photoshop docs. \n\n"
    #                           f"Remember to be courteous with all members. \n"
    #                           f"(No, there is no difference between <#{constants.alpha}> and <#{constants.beta}>)",
    #                     inline=False)

        # embed = Embed(
        #         title=f"Unsupported help topics",
        #         color=constants.blurple)
        #
        # embed.add_field(name=f"Editing requests of any nature ",
        #                 value=f"As per the server rules, we have no interest in maintaining such a feature, nor "
        #                       f"do we have the resources necessary to facilitate commissions and protect both the "
        #                       f"buyer and seller. ",
        #                 inline=False)
        #
        # embed.add_field(name=f"Demands of needing a private, one-on-one tutor  ",
        #                 value=f"In addition to technical expertise, one of the crucial skills of being a good "
        #                       f"Photoshopper is self-sufficiency. We will be happy to answer any technical questions, "
        #                       f"but we believe Photoshop is absolutely a software anyone can master "
        #                       f"on their own. \n",
        #                 inline=False)
        #
        # embed.add_field(name=f"Asking for help finding step-by-step video tutorials, or asking for spoonfeeding",
        #                 value=f"We're not a YouTube search bar. If you want to know what an effect is called or how "
        #                       f"to replicate it, we will give you our suggestions. It is up to you to find and "
        #                       f"learn from those suggestions, preferably from the docs first. ",
        #                 inline=False)
        #
        # embed.add_field(name=f"Inappropriate works ",
        #                 value=f"As per the server rules, anything that may be considered illicit, malicious, or "
        #                       f"downright not safe for work (NSFW) does not belong here.",
        #                 inline=False)
        #
        # embed.add_field(name=f"Assistance with closed assessments",
        #                 value=f"We will not help with closed assessments, such as quizzes, tests, and exams. "
        #                       f"General guidance on homework and assignments is allowed.",
        #                 inline=False)
        #
        # embed.add_field(name=f"Recognition of fonts",
        #                 value=f"We are not a font recognition engine. Please see `!tag wfit` instead.",
        #                 inline=False)
        #
        # embed.add_field(name=f"Recognition of whether an image is Photoshopped",
        #                 value=f"Who knows?",
        #                 inline=False)

        # embed.set_thumbnail(url="https://i.postimg.cc/hj4bVZwg/ISW-EAR.png")

        # await ctx.send(embed=embed)

    @commands.command()
    async def just(self, ctx):
        showcase = self.bot.get_channel(constants.showcase)
        msg = await showcase.fetch_message(873283487841529906)
        await msg.delete()
        await showcase.send(f"<@756906081829126245>, direct social media links are not permitted. If you have "
                            f"pictures, you should send them here directly instead of compelling others to visit "
                            f"an external site.")

    @commands.command()
    async def promote(self, ctx: commands.Context, member: discord.Member):
        print(ctx.channel)

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
