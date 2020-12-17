import discord
import traceback
import sys
import random
from discord.ext import commands
from discord.utils import get

class Announce(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def announce(self, ctx, channel, *, title):
 
        chars = "<#>"

        for char in chars:
            channel = channel.replace(char, "") # direct id grabber
            
        channelname = self.bot.get_channel(int(channel))
        channelname = str(channelname)
        channel = discord.utils.get(ctx.guild.channels, name=channelname)
        
        await ctx.send("Header has been set. Now type body.")
        def check(message):
                return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id
    
        body = await self.bot.wait_for('message', check=check)

        embed=discord.Embed()

        embed.add_field(name=str(title), value=body.content, inline=False)
        # embed.set_thumbnail(url=ctx.author.avatar_url) 
        await channel.send(embed=embed)

        #embed.set_thumbnail(url=ctx.author.avatar_url) medium image no
        #embed.set_image(url=ctx.author.avatar_url) huge image we don't want this
        

    

def setup(bot):
    bot.add_cog(Announce(bot))