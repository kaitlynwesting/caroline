import discord
import requests
import asyncio
from discord.ext import commands
from discord.utils import get

import traceback
import sys, string
import random
import emoji

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def topic(self, ctx):

        fin = open("cogs/texts/prompts.txt", "r")
        lines = fin.readlines()

        question = random.choice(lines)

        embed=discord.Embed()

        embed.add_field(name=str("A random topic..."), value=f"{question}", inline=False)
        embed.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        print(question)


    @commands.command()
    async def wyr(self, ctx):

        question = requests.get('http://either.io/questions/next').json()['questions'][0]

        one = int(question['option1_total']) 
        two = int(question['option2_total']) 
        
        onePer = round((one / (one + two)) * 100, 2)
        twoPer = round((two / (one + two)) * 100, 2)

        onePop = int(question['option1_total'])
        twoPop = int(question['option2_total'])

        embed = discord.Embed(title="Would You Rather...")
        embed.set_author(name=f"Requested by {ctx.author.display_name}\n{question['slug'].replace('-', ' ').upper()} by {question['display_name']} ", icon_url=ctx.author.avatar_url)
        embed.add_field(name=f"{question['option_1']}", value=f"{onePer}% ({onePop:,} voted)")
        embed.add_field(name=f"{question['option_2']}", value=f"{twoPer}% ({twoPop:,} voted)")

        embedio = await ctx.send(embed=embed)

        await embedio.add_reaction(emoji="🅰️")
        await embedio.add_reaction(emoji="🅱️")
    

    # SPECIAL "MOCK" COMMAND TO COMMEMORATE CODE BASH ONE (THONKS TO CHILD!)
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def mock(self, ctx, message):

        newStr = ""
        lastCase = True

        for char in str(ctx.message.content).strip('\n'):
            newChar = char if char in string.punctuation or char == " " else char.lower() if lastCase else char.upper() 
            if (not char in string.punctuation) and (not char == " "): lastCase = not lastCase
            newStr += newChar

        await ctx.channel.purge(limit=1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True)
        await ctx.send (newStr[5:])

def setup(bot):
    bot.add_cog(Fun(bot))