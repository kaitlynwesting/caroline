import discord
from discord.ext import tasks, commands
from discord.utils import get
from datetime import datetime, timezone, timedelta
import pytz

import traceback
import sys
import random

class Notification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    
    # LOOP TO CHECK FOR DORMANT HELP CHANNELS 
    @tasks.loop(seconds=1)
    async def help_dormant(self):
        channelList = [780519472444080158, 777207889277616192] # hardcoded two help channels, unfortunately can't get channel by names, doesn't support it

        for channel in channelList:
            channel = self.bot.get_channel(channel)

            async for message in channel.history(limit=1):
                
                if message.author == self.bot.user:
                    pass
                else:
                    # print(message.content)

                    nowTime = datetime.now(tz=timezone.utc)
                    messageTime = pytz.utc.localize(message.created_at)
                    duration = nowTime - messageTime
                    threshold = timedelta(hours=4) # how long before channel marked as inactive?

                    if duration >= threshold:
                        print("Hmm...")
                        embed=discord.Embed(
                        # title = "This is a test", 
                        color=0x349feb
                        )

                        embed.set_author(name=f"Open help channel", icon_url="https://i.postimg.cc/BZMpHQQV/image5.jpg")

                        embed.add_field(
                        name=f"Some tips to keep in mind before you ask:", 
                        value=f"""• Refrain from asking generic or vague questions, such as "Can I get help" or "Why isn't this working".
• Explain what you're trying to do, what you have tried, and the outcome. This greatly facilitates the work of any potential helpers.
• Include a screenshot or snip of your Photoshop workspace, if appropriate.""", 
                        inline=False)
                        embed.set_footer(text="Others will try to help you solve the problem, if they can. Sit tight!")
                        
                        await message.channel.send(embed=embed) 
                    else:
                        pass
            
    
    # CLOSE HELP CHANNEL MANUALLY
    @commands.command()
    async def close(self, ctx):
        channelList = [780519472444080158, 777207889277616192]

        if ctx.channel.id in channelList:
            embed=discord.Embed(
                            color=0x349feb
                            )

            embed.set_author(name=f"Open help channel", icon_url="https://i.postimg.cc/BZMpHQQV/image5.jpg")

            embed.add_field(
            name=f"Some tips to keep in mind before you ask:", 
            value=f"""• Refrain from asking generic or vague questions, such as "Can I get help" or "Why isn't this working".
• Explain what you're trying to do, what you have tried, and the outcome. This greatly facilitates the work of any potential helpers.
• Include a screenshot or snip of your Photoshop workspace, if appropriate.""", 
            inline=False)
            embed.set_footer(text="Others will try to help you solve the problem, if they can. Sit tight!")
            
            await ctx.send(embed=embed) 
        
        else:
            await ctx.send("Please use that in the proper channels, i.e. our help channels.")


    # TOGGLE RULES FOR DUMMIES
    @commands.command(aliases=["rules"])
    async def rule(self, ctx, number=None):

        ruleContent = ""
        ruleNums = ['1', '2', '3', '4', '5', '6',]

        with open('cogs/texts/rules.txt', 'r') as f:
            rules = f.readlines()

        if number == None:

            embed=discord.Embed(
            title = "Photoshop Discord Rules",
            color=0x349feb,
            description = "We expect all members of our community to understand and abide by our rules, which can be found in the <#777237462904209429> channel.", 
            inline=False
            )
            await ctx.send(embed=embed)
            
        else:
            
            if number not in ruleNums:
            
                embed=discord.Embed(
                title = "Photoshop Discord Rules",
                description = "No such rule exists.",
                color = 0x349feb
                )
                await ctx.send(embed=embed)
            
            else:

                embed=discord.Embed(
                title = "Photoshop Discord Rules", 
                color=0x349feb
                )

                embed.add_field(name=f"Rule {number}: ", value=f'{rules[(int(number) + 1) * 2]}', inline=False)
                await ctx.send(embed=embed)
    

    # LOOP TO CHECK FOR BUMPING TIMES 
    @tasks.loop(seconds=10)
    async def printer(self):
        all_ready = []

        botcommands = await self.bot.fetch_channel(787090740517273680) # bot-commands
        lobby = await self.bot.fetch_channel(777207889277616191) # lobby

        async for message in botcommands.history(limit=100):
            if len(message.embeds) > 0:
                    if message.author.id == 302050872383242240: # This is Disboard's profile ID.
                        
                        if "Bump done" in message.embeds[0].description:

                            time_now = datetime.now(tz=timezone.utc)
                            time_message = pytz.utc.localize(message.created_at)
                            duration = time_now - time_message
                            bump_threshold = timedelta(hours=2)                               
                            all_ready.append(True if duration > bump_threshold else False)
        
        async for message in lobby.history(limit=100):
            if "Do `!d bump`" in message.content:

                time_now = datetime.now(tz=timezone.utc)
                time_message = pytz.utc.localize(message.created_at)
                duration = time_now - time_message
                reminder_threshold = timedelta(minutes=60)                               
                all_ready.append(True if duration > reminder_threshold else False)
                                
        
        send_reminder = False if False in all_ready else True
        if send_reminder == True:
            await lobby.send("It's time to bump! Do `!d bump` in our <#787090740517273680> channel!")
            

                
    # CHECC PING
    @commands.command()
    async def ping(self, ctx):

        await ctx.send(f"Pong! The latency is {round(self.bot.latency, 3)} milliseconds.")


def setup(bot):
    bot.add_cog(Notification(bot))