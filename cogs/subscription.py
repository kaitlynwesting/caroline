import discord
from discord.ext import commands
from discord.utils import get

import traceback
import sys
import random

class Subscription(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # INSUFFICIENT PARAMETERS
    @commands.command()
    async def subscribe(self, ctx, message):

        if (message == "totd"):
            if get(ctx.guild.roles, name="Tip of the Day"):
                totd = get(ctx.guild.roles, name="Tip of the Day")

                if totd in ctx.author.roles: # check if they already have role
                    await ctx.send(f"You have already subscribed to this!")
                else:
                    await ctx.author.add_roles(totd)
                    await ctx.send(f"{ctx.author.display_name}, you've subscribed to our daily tips!") #tag actual channel here in real server
            else:
                await ctx.guild.create_role(name="Tip of the Day", colour=discord.Colour(0xB9BBBE)) # make new role if not existing, omfg the colour
                totd = get(ctx.guild.roles, name="Tip of the Day")
                await ctx.author.add_roles(totd)
                await ctx.send(f"{ctx.ctx.author.display_name}, you've subscribed to our daily tips!")
        else:
            await ctx.send("Hmm, we don't offer that subscription yet. Perhaps you meant something else?")

def setup(bot):
    bot.add_cog(Subscription(bot))