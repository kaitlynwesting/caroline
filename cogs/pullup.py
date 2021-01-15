import discord
from discord.ext import tasks, commands
from discord.utils import get
from datetime import datetime, timezone, timedelta
import pytz

import traceback
import sys
import random

class Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    
    # LOOP TO CHECK FOR DORMANT HELP CHANNELS 
    @tasks.loop(seconds=60)
    async def printer(self):
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

                        embed.set_author(name=f"Open help channel", icon_url="https://filebin.net/eqom39vn27int15t/image5.jpg?t=81mfvzfn")

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

            embed.set_author(name=f"Open help channel", icon_url="https://filebin.net/eqom39vn27int15t/image5.jpg?t=81mfvzfn")

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

    

def setup(bot):
    bot.add_cog(Handler(bot))