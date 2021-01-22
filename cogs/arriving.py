import asyncio

import discord
from discord.ext import commands
from discord.utils import get

import emoji
from io import BytesIO
import os
import random
import requests
import sys
import time
import traceback

# COG FOR NEW ARRIVALS AND DEPARTS

class Rules(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot 


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        guild = self.bot.get_guild(payload.guild_id)
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = guild.get_member(payload.user_id)
        emoji = payload.emoji

        lobby = discord.utils.get(guild.channels, name="lobby")
        creator = get(guild.roles, name="Creator")
        muted = get(guild.roles, name="Muted")

        fin = open("cogs/texts/prompts.txt", "r")
        questionList = fin.readlines()

        fin = open("cogs/texts/join.txt", "r")
        joinMessageList = fin.readlines()

        question = random.choice(questionList)
        joinMessage = random.choice(joinMessageList)
        joinMessage = joinMessage.replace("username", f"{member.name}")

        if channel.name == "rules":
            if muted in member.roles:
                await channel.send(f"Uhh, {member.mention}, you're muted.", delete_after = 3)
            elif creator in member.roles:
                await channel.send(f"{member.mention}, you're already a creator!", delete_after = 3)

            else:
                await member.add_roles(creator)
                await channel.send(f"{member.name}, thanks for accepting our rules! Welcome to Photoshop Discord!", delete_after = 3)

                embed=discord.Embed(color = 0x349feb)

                embed.add_field(name=f"{joinMessage}", value=f"Here's an icebreaker for you, {member.mention}: 🍬 {question}", inline=False)
                embed.set_author(name=f"{member.name} joined the server!", icon_url=member.avatar_url)
                await lobby.send(embed=embed)


    # DELETE IRRELEVANT CONTENT IN RULES CHANNEL
    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel) == "rules": 
            if message.author.id == 669977303584866365 or message.author.id == 785298572047417374: # my id and lydia's id, idk if there's a message.author.role
                pass
            elif str(message.channel) == "rules" and message.content == ".accept":
                pass
            else:
                await message.delete()
        
    # JOIN LOGGER
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="logs") # THIS IS TERRIFIC <---
        await channel.send(f"{member.mention} has joined us.")

    # LEAVE LOGGER
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="logs") # THIS IS TERRIFIC <---
        await channel.send(f"{member.mention} has left.")
    
            

# binds the cog to the client file
def setup(bot):
    bot.add_cog(Rules(bot)) 



