import discord
import asyncio
from discord.ext import commands
from discord.utils import get

import traceback
import sys
import random
import emoji

# COG FOR NEW ARRIVALS AND DEPARTS

class Rules(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot 


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        fin = open("cogs/texts/prompts.txt", "r")
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
                

                welcome = [f"{member.name} just joined the server - glhf!",
                    f"{member.name} just joined. Everyone, look busy!",
                    f"{member.name} just joined. Can I get a heal?",
                    f"{member.name} joined your party.",
                    f"{member.name} joined. You must construct additional pylons.",
                    f"Ermagherd. {member.name} is here.",
                    f"Welcome, {member.name}. Stay awhile and listen.",
                    f"Welcome, {member.name}. We were expecting you ( ͡° ͜ʖ ͡°)",
                    f"Welcome, {member.name}. We hope you brought pizza.",
                    f"Welcome {member.name}. Leave your weapons by the door.",
                    f"A wild {member.name} appeared.",
                    f"Swoooosh. {member.name} just landed.",
                    f"Brace yourselves. {member.name} just joined the server.",
                    f"{member.name} just joined. Hide your bananas.",
                    f"{member.name} just arrived. Seems OP - please nerf.",
                    f"{member.name} just slid into the server.",
                    f"A {member.name} has spawned in the server.",
                    f"Big {member.name} showed up!",
                    f"Where’s {member.name}? In the server!",
                    f"{member.name} hopped into the server. Kangaroo!!",
                    f"{member.name} just showed up. Hold my beer.",
                    f"Challenger approaching - {member.name} has appeared!",
                    f"It's a bird! It's a plane! Nevermind, it's just {member.name}.",
                    f"It's {member.name}! Praise the sun! [T]/",
                    f"Never gonna give {member.name} up. Never gonna let {member.name} down.",
                    f"Ha! {member.name} has joined! You activated my trap card!",
                    f"Cheers, love! {member.name}'s here!",
                    f"Hey! Listen! {member.name} has joined!",
                    f"We've been expecting you, {member.name}",
                    f"It's dangerous to go alone, take {member.name}!",
                    f"{member.name} has joined the server! It's super effective!",
                    f"Cheers, love! {member.name} is here!",
                    f"{member.name} is here, as the prophecy foretold.",
                    f"{member.name} has arrived. Party's over.",
                    f"Ready player {member.name}",
                    f"{member.name} is here to kick butt and chew bubblegum. And {member.name} is all out of gum.",
                    f"Hello. Is it {member.name} you're looking for?",
                    f"{member.name} has joined. Stay a while and listen!",
                    f"Roses are red, violets are blue, {member.name} joined this server with you"]
                

                embed=discord.Embed()

                embed.add_field(name=f"{random.choice(welcome)}", value=f"Here's an icebreaker for you, {member.mention}: 🍬 {question}", inline=False)
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
    
    # TOGGLE RULES FOR DUMMIES
    @commands.command(aliases=["rules"])
    async def rule(self, ctx, *, number=None):

        def cutString(bigString):
            bigString = bigString.replace('\n', ' ')
            return bigString
        
        global myStr

        if number == None:

            embed=discord.Embed(
            title = "Rules of Photoshop Discord",
            color=0x349feb,
            description = cutString("""We expect all members of our community to understand and abide by our rules, 
which can be found in the <#777237462904209429> channel."""), 
            inline=False
            )
            
            await ctx.send(embed=embed)

        else:
            number = str(number)

            if number == '1':

                embed=discord.Embed(
                title = "Rules of Photoshop Discord", 
                # url = "https://canary.discord.com/channels/777207888846389270/777237462904209429/791682685515857920",
                color=0x349feb
                )

                embed.add_field(
                name=f"Rule {number}: ", 
                value=f"Follow the [Discord Community Guidelines](https://discord.com/guidelines) and [Terms of Service](https://discord.com/terms).", 
                inline=False)
            
                await ctx.send(embed=embed)

                return
            elif number == '2':
                myStr = (cutString("""Behave maturely and respectfully towards other members of the community."""))
            
            elif number == '3':
                myStr = (cutString("""Listen to and respect staff members and their directions."""))
            
            elif number == '4':
                myStr = (cutString("""This is an English-speaking server. Please speak English to the best of your ability."""))
                
            elif number == '5':
                myStr = (cutString("""Do not request help with or post projects that may be considered illicit,
breach terms of services, malicious or inappropriate (such as NSFW). Use common sense and judgement."""))

            elif number == '6':
                myStr = (cutString("""No spamming or advertising, including requests or commissions. 
**We are not a charity case; we will not create anything for you.**"""))
            
            else:
                embed=discord.Embed(
                title = "Rules of Photoshop Discord",
                description = "No such rule exists.",
                color = 0x349feb
                )
                await ctx.send(embed=embed)

                return

            embed=discord.Embed(
            title = "Rules of Photoshop Discord", 
            color=0x349feb
            )

            embed.add_field(name=f"Rule {number}: ", value=f'{myStr}', inline=False)
            
            await ctx.send(embed=embed) 

            

# binds the cog to the client file
def setup(bot):
    bot.add_cog(Rules(bot)) 



