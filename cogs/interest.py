import discord
import requests
import asyncio
from discord.ext import commands
from discord.utils import get

import traceback
import sys
import random
import emoji

class Interest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def topic(self, ctx):

        fin = open("cogs/start.txt", "r")
        lines = fin.readlines()

        question = random.choice(lines)

        embed=discord.Embed()

        embed.add_field(name=str("A random topic..."), value=f"{question}", inline=False)
        embed.set_author(name=" ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        print(question)
        await ctx.send(question)
        # await ctx.send(question) 


    @commands.command()
    async def wyr(self, ctx):

        question = requests.get('http://either.io/questions/next').json()['questions'][0]
        embed = discord.Embed(title="Would You Rather?") #, color=0x001E36)
        embed.add_field(name="A", value=question['option_1'])
        embed.add_field(name="B", value=question['option_2'])

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Interest(bot))