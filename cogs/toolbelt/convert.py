# from PIL import Image
# im = Image.open('../../media/ss.webp').convert('RGB')
# im.save('ss.png', 'png')

import discord
from discord.ext import commands
from PIL import Image


class Convert(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def convert(self, ctx):

        return

    @convert.command()
    @commands.guild_only()
    async def png(self, ctx):

        if ctx.message.attachments[0].filename.endswith('png'):
            await ctx.send("That's already a png!")
            return

        if ctx.message.attachments[0].filename.endswith(
                ('jpg',
                 'jpeg',
                 'webp',
                 'bmp',
                 'cr2',
                 'dng',
                 'heic',
                 'svg'
                 )
        ) is False:
            await ctx.send("Are you trying to kill me?")
            return

        await ctx.message.attachments[0].save('media/temp.png')
        await ctx.send("Here you go!", file=discord.File("media/temp.png"))


def setup(bot):
    bot.add_cog(Convert(bot))
