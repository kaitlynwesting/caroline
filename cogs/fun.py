import asyncio
from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands
from discord.utils import get

import os
import pytz
import random
import requests
import sys
import string
import time
import traceback

# COG FOR GENERAL "FUN" COMMANDS

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Bread command mutes the user for smelliness.
    @commands.command()
    async def bread(self, ctx):

        announcements = get(ctx.guild.roles, name="Announcements")
        totd = get(ctx.guild.roles, name="Tip of the Day")

        creator = get(ctx.guild.roles, name="Creator")
        muted = get(ctx.guild.roles, name="Muted")
        
        # Remove all roles, except for subscription roles.
        for role in ctx.author.roles:
            try:
                if role == announcements or role == totd:
                    pass
                else:
                    await ctx.author.remove_roles(role)
            except Exception as e:
                pass

        # Apply muted role to the bread user and send a small notification.
        await ctx.author.add_roles(muted)  
        await ctx.send(f"📨 Applying **tempmute** to {ctx.author.mention} for 10s (Reason: insufficient hygiene).")

        # Wait for 10 seconds.
        await asyncio.sleep(10)

        # If the user still has this role, then remove it and send a small notification.
        if muted in ctx.author.roles:
            await ctx.author.remove_roles(muted)
            await ctx.author.add_roles(creator)
         
            await ctx.send(f"📨 {ctx.author.mention} has been automatically **unmuted** now. Shower next time.") 


    # Generates a random topic for discussion.
    @commands.command()
    async def topic(self, ctx):

        fin = open("cogs/texts/prompts.txt", "r")
        lines = fin.readlines()

        question = random.choice(lines)

        # Generate a nice question embed, and send it.
        embed=discord.Embed()

        embed.add_field(name=str("A random topic..."), value=f"{question}", inline=False)
        embed.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


    # Generates a random would-you-rather for discussion.
    @commands.command()
    async def wyr(self, ctx):

        # Grab the questions from here.
        question = requests.get('http://either.io/questions/next').json()['questions'][0]

        # Calculate total number of people selecting each choice.
        one = int(question['option1_total']) 
        two = int(question['option2_total']) 
        
        # Calculate percentages of people who have selected each choice.
        onePer = round((one / (one + two)) * 100, 2)
        twoPer = round((two / (one + two)) * 100, 2)

        embed = discord.Embed(title="Would You Rather...")
        embed.set_author(name=f"Requested by {ctx.author.display_name}\n{question['slug'].replace('-', ' ').upper()} by {question['display_name']} ", icon_url=ctx.author.avatar_url)
        embed.add_field(name=f"{question['option_1']}", value=f"{onePer}% ({one:,} voted)")
        embed.add_field(name=f"{question['option_2']}", value=f"{twoPer}% ({two:,} voted)")

        embedio = await ctx.send(embed=embed)

        # React with two choices for selection.
        await embedio.add_reaction(emoji="🅰️")
        await embedio.add_reaction(emoji="🅱️")
    

    # A special "mock" command to commemorate Child's mock case.
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