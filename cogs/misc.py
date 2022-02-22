import asyncio
from discord.ext import commands
from discord import Embed
import discord
import traceback
from cogs.utils import constants
from cogs.utils.buttons import PaginationView


class EmbedFlags(commands.FlagConverter, prefix='--', delimiter=' '):
    title: str = ""
    description: str = ""
    image: str = ""
    footer: str = ""
    colour: str = constants.blurple


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def embed(self, ctx, *, flags: EmbedFlags):
        """
        A utility to create embeds via command.
        """

        if type(flags.colour) == str:
            flags.colour = int(f"{flags.colour}", 16)

        embed = discord.Embed()

        try:
            embed = embed.from_dict({'title': f'{flags.title}',
                                     'description': f'{flags.description}',
                                     'image': {'url': f'{flags.image}'},
                                     'footer': {'text': f'{flags.footer}'},
                                     'color': flags.colour,
                                     })
            await ctx.send("**This is a preview of your embed. Which channel do you want to send it in?**", embed=embed)
        except discord.errors.HTTPException as error:
            if error.code == 50035:  # cannot send nothing
                traceback.print_exception(type(error), error, error.__traceback__)
                return await ctx.send("Embed cannot be empty. Aborted.")
            else:
                raise

        def check(message):
            return message.author.id == ctx.author.id and \
                   message.channel.id == ctx.channel.id

        try:
            response = await self.bot.wait_for('message', check=check, timeout=60)
            channel = await commands.TextChannelConverter.convert(self.bot, ctx, response.content)
            await channel.send(embed=embed)

        except Exception as error:
            if type(error) == commands.errors.ChannelNotFound:
                return await ctx.send("Could not convert to a text channel. Aborted.")
            elif type(error) == asyncio.exceptions.TimeoutError:
                return await ctx.send("Took too long. Aborted.")
            else:
                raise

    # @commands.command(aliases=["ce"])
    # @commands.has_permissions(administrator=True)
    # async def change_existing(self, ctx, target_channel, target_message_id):
    #     rules = self.bot.get_channel(target_channel)
    #     msg = await rules.fetch_message(target_message_id)
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

def setup(bot):
    bot.add_cog(Misc(bot))
