import asyncio

import discord
from discord.ext import commands

import random
import requests
import string
from utils import constants


# COG FOR GENERAL "FUN" COMMANDS

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # BREAD COMMAND WHICH MUTES THE USER FOR SMELLINESS.
    @commands.command()
    async def bread(self, ctx):

        muted = ctx.guild.get_role(constants.muted)

        # Remove all roles, except for subscription roles.
        for role in ctx.author.roles:
            try:
                await ctx.author.remove_roles(role)
            except Exception as e:
                pass

        # Apply muted role to the bread user and send a small notification.
        await ctx.author.add_roles(muted)
        await ctx.send(f"📨 Applying **tempmute** to {ctx.author.mention} for 10s (Reason: insufficient hygiene).")

        # Wait for 10 seconds.
        await asyncio.sleep(10)

        if muted in ctx.author.roles:
            await ctx.author.remove_roles(muted)

            await ctx.send(f"📨 {ctx.author.mention} has been automatically **unmuted** now. Shower next time.")


    @commands.command()
    async def topic(self, ctx):

        fin = open("cogs/texts/prompts.txt", "r")
        lines = fin.readlines()

        question = random.choice(lines)

        # Generate a nice question embed, and send it.
        embed = discord.Embed()

        embed.add_field(name=str("A random topic..."), value=f"{question}", inline=False)
        embed.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    # RANDOM WOULD-YOU-RATHER GENERATOR.
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
        embed.set_author(
            name=f"Requested by {ctx.author.display_name}\n{question['slug'].replace('-', ' ').upper()} by {question['display_name']} ",
            icon_url=ctx.author.avatar_url)
        embed.add_field(name=f"{question['option_1']}", value=f"{onePer}% ({one:,} voted)")
        embed.add_field(name=f"{question['option_2']}", value=f"{twoPer}% ({two:,} voted)")

        embedio = await ctx.send(embed=embed)

        # React with two choices for selection.
        await embedio.add_reaction(emoji="🅰️")
        await embedio.add_reaction(emoji="🅱️")

    # A SPECIAL "MOCK" COMMAND TO COMMEMORATE CHILD'S MOCKCASE.
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mock(self, ctx, message):

        newStr = ""
        lastCase = True

        for char in str(ctx.message.content).strip('\n'):
            newChar = char if char in string.punctuation or char == " " else char.lower() if lastCase else char.upper()
            if (not char in string.punctuation) and (not char == " "): lastCase = not lastCase
            newStr += newChar

        await ctx.channel.purge(limit=1, check=None, before=None, after=None, around=None, oldest_first=False,
                                bulk=True)
        await ctx.send(newStr[5:])


def setup(bot):
    bot.add_cog(Fun(bot))
