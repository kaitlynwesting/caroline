import discord
from discord.ext import commands
from discord.utils import get

import sys
import traceback

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # [INACTIVE] For editing the rule embed.
    """ @commands.command()
    @commands.has_permissions(administrator = True)
    async def edit(self, ctx):
        
        msg = await ctx.fetch_message(791682685515857920)
        
        with open('cogs/texts/rules.txt', 'r') as f:
            rules = f.read()

        embed=discord.Embed (
        title = f"Photoshop Discord Rules", 
        color=0x349feb, 
        description=rules)
        
        embed.set_thumbnail(url="https://i.postimg.cc/bJSGjhD5/IDEK.png")

        # embed.add_field(name="HEEHEE", value="LOL", inline=False)
        #await channel.send(embed=embed)

        await msg.edit(embed=embed) """
        

def setup(bot):
    bot.add_cog(Misc(bot))