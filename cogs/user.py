import discord
import traceback
import sys
import random
from discord.ext import commands

class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def avatar(self, ctx, member: discord.Member=None):

        embed=discord.Embed(color=0x349feb)
                        
        if member == None:
            member = ctx.author

        embed.set_image(url=member.avatar_url)

        if str(member.display_name)[-1] == "s": 
            embed.set_author(name=f"{member.display_name}' avatar:", icon_url=member.avatar_url)
        else:
            embed.set_author(name=f"{member.display_name}'s avatar:", icon_url=member.avatar_url)

        await ctx.send(embed=embed) 

    
def setup(bot):
    bot.add_cog(User(bot))