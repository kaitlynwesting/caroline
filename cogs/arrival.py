import discord
import asyncio
from discord.ext import commands
from discord.utils import get

import traceback
import sys
import random
import emoji

# COG FOR NEW ARRIVALS AND DEPARTS

class Arrival(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot 

    """ # ACCEPT RULES
    @commands.command()
    async def accept(self, ctx):
        if ctx.channel.name == "rules":
            if get(ctx.guild.roles, name="Creator"):
                creator = get(ctx.guild.roles, name="Creator")
                muted = get(ctx.guild.roles, name="Muted")

                if creator in ctx.author.roles: # already has role
                    await ctx.message.delete()
                    message = await ctx.send(f"You have already accepted the rules!", delete_after=5)
                elif muted in ctx.author.roles: # to catch people who are trying to bypass muted
                    await ctx.message.delete()
                    await ctx.send(f"Trying to bypass your mute, {ctx.author.mention}? That wasn't very smart of you, was it?", delete_after=5) 
                else:
                    await ctx.author.add_roles(creator) # add creator role
                    # await asyncio.sleep(1)
                    await ctx.message.delete()
                    await ctx.send(f"{ctx.author.name}, thanks for accepting our rules! Welcome to Photoshop Discord!", delete_after=5)

                    channel = discord.utils.get(ctx.guild.channels, name="lobby") 
                    welcome = [f"{ctx.author.mention} just joined the server - glhf!",
                    f"{ctx.author.mention} just joined. Everyone, look busy!",
                    f"{ctx.author.mention} just joined. Can I get a heal?",
                    f"{ctx.author.mention} joined your party.",
                    f"{ctx.author.mention} joined. You must construct additional pylons.",
                    f"Ermagherd. {ctx.author.mention} is here.",
                    f"Welcome, {ctx.author.mention}. Stay awhile and listen.",
                    f"Welcome, {ctx.author.mention}. We were expecting you ( ͡° ͜ʖ ͡°)",
                    f"Welcome, {ctx.author.mention}. We hope you brought pizza.",
                    f"Welcome {ctx.author.mention}. Leave your weapons by the door.",
                    f"A wild {ctx.author.mention} appeared.",
                    f"Swoooosh. {ctx.author.mention} just landed.",
                    f"Brace yourselves. {ctx.author.mention} just joined the server.",
                    f"{ctx.author.mention} just joined. Hide your bananas.",
                    f"{ctx.author.mention} just arrived. Seems OP - please nerf.",
                    f"{ctx.author.mention} just slid into the server.",
                    f"A {ctx.author.mention} has spawned in the server.",
                    f"Big {ctx.author.mention} showed up!",
                    f"Where’s {ctx.author.mention}? In the server!",
                    f"{ctx.author.mention} hopped into the server. Kangaroo!!",
                    f"{ctx.author.mention} just showed up. Hold my beer.",
                    f"Challenger approaching - {ctx.author.mention} has appeared!",
                    f"It's a bird! It's a plane! Nevermind, it's just {ctx.author.mention}.",
                    f"It's {ctx.author.mention}! Praise the sun! [T]/",
                    f"Never gonna give {ctx.author.mention} up. Never gonna let {ctx.author.mention} down.",
                    f"Ha! {ctx.author.mention} has joined! You activated my trap card!",
                    f"Cheers, love! {ctx.author.mention}'s here!",
                    f"Hey! Listen! {ctx.author.mention} has joined!",
                    f"We've been expecting you, {ctx.author.mention}",
                    f"It's dangerous to go alone, take {ctx.author.mention}!",
                    f"{ctx.author.mention} has joined the server! It's super effective!",
                    f"Cheers, love! {ctx.author.mention} is here!",
                    f"{ctx.author.mention} is here, as the prophecy foretold.",
                    f"{ctx.author.mention} has arrived. Party's over.",
                    f"Ready player {ctx.author.mention}",
                    f"{ctx.author.mention} is here to kick butt and chew bubblegum. And {ctx.author.mention} is all out of gum.",
                    f"Hello. Is it {ctx.author.mention} you're looking for?",
                    f"{ctx.author.mention} has joined. Stay a while and listen!",
                    f"Roses are red, violets are blue, {ctx.author.mention} joined this server with you"]
                    
                    await channel.send(random.choice(welcome))
                    
        else:
            await ctx.send("Why are you accepting again?") """


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        fin = open("cogs/start.txt", "r")
        lines = fin.readlines()

        question = random.choice(lines)

        guild = self.bot.get_guild(payload.guild_id)
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = guild.get_member(payload.user_id)
        emoji = payload.emoji

        print(member)

        lobby = discord.utils.get(guild.channels, name="lobby")
        creator = get(guild.roles, name="Creator")
        muted = get(guild.roles, name="Muted")

        if channel.name == "rules":
            if muted in member.roles:
                await channel.send(f"Uhh, {member.mention}, you're muted.", delete_after = 3)
            elif creator in member.roles:
                await channel.send(f"{member.mention}, you're already a creator!", delete_after = 3)
            else:
                print(emoji)
                await member.add_roles(creator) # add creator role
                await channel.send(f"{member.name}, thanks for accepting our rules! Welcome to Photoshop Discord!", delete_after = 4)
                
                welcome = [f"{member.mention} just joined the server - glhf!",
                    f"{member.mention} just joined. Everyone, look busy!",
                    f"{member.mention} just joined. Can I get a heal?",
                    f"{member.mention} joined your party.",
                    f"{member.mention} joined. You must construct additional pylons.",
                    f"Ermagherd. {member.mention} is here.",
                    f"Welcome, {member.mention}. Stay awhile and listen.",
                    f"Welcome, {member.mention}. We were expecting you ( ͡° ͜ʖ ͡°)",
                    f"Welcome, {member.mention}. We hope you brought pizza.",
                    f"Welcome {member.mention}. Leave your weapons by the door.",
                    f"A wild {member.mention} appeared.",
                    f"Swoooosh. {member.mention} just landed.",
                    f"Brace yourselves. {member.mention} just joined the server.",
                    f"{member.mention} just joined. Hide your bananas.",
                    f"{member.mention} just arrived. Seems OP - please nerf.",
                    f"{member.mention} just slid into the server.",
                    f"A {member.mention} has spawned in the server.",
                    f"Big {member.mention} showed up!",
                    f"Where’s {member.mention}? In the server!",
                    f"{member.mention} hopped into the server. Kangaroo!!",
                    f"{member.mention} just showed up. Hold my beer.",
                    f"Challenger approaching - {member.mention} has appeared!",
                    f"It's a bird! It's a plane! Nevermind, it's just {member.mention}.",
                    f"It's {member.mention}! Praise the sun! [T]/",
                    f"Never gonna give {member.mention} up. Never gonna let {member.mention} down.",
                    f"Ha! {member.mention} has joined! You activated my trap card!",
                    f"Cheers, love! {member.mention}'s here!",
                    f"Hey! Listen! {member.mention} has joined!",
                    f"We've been expecting you, {member.mention}",
                    f"It's dangerous to go alone, take {member.mention}!",
                    f"{member.mention} has joined the server! It's super effective!",
                    f"Cheers, love! {member.mention} is here!",
                    f"{member.mention} is here, as the prophecy foretold.",
                    f"{member.mention} has arrived. Party's over.",
                    f"Ready player {member.mention}",
                    f"{member.mention} is here to kick butt and chew bubblegum. And {member.mention} is all out of gum.",
                    f"Hello. Is it {member.mention} you're looking for?",
                    f"{member.mention} has joined. Stay a while and listen!",
                    f"Roses are red, violets are blue, {member.mention} joined this server with you"]
                
                embed=discord.Embed()

                embed.add_field(name=str("Welkom!"), value=f"{random.choice(welcome)}\n {question}", inline=False)
                embed.set_author(name=f"{member.display_name} joined the server!", icon_url=member.avatar_url)
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
    bot.add_cog(Arrival(bot)) 



