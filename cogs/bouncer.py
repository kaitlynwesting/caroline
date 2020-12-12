import discord
import traceback
import sys
import random
import datetime

from discord.utils import get
from discord.ext import commands

class Bouncer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # BOUNCELIST OF PEOPLE WHO HAVE NOT ACCEPTED
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def bouncelist(self, ctx): # reason is not None as warnings must be meaningful
        
        creator = get(ctx.guild.roles, name="Creator")
        muted = get(ctx.guild.roles, name="Muted")
        channel = discord.utils.get(ctx.guild.channels, name="logs") 
        bots = get(ctx.guild.roles, name="Bots")

        i = 0
        array = []
        dormant = 0

        message = await ctx.send("The following is a list of users without a role, who have been in the server for more than one week:")
        
        for member in ctx.guild.members:
            x = datetime.datetime.now()
            y = member.joined_at
            z = x - y

            zday = z.days
            zhour = round(z.seconds/3600, 2)

            if (zday > 7):
                if creator in member.roles or muted in member.roles or bots in member.roles:
                    pass
                elif (zday == 1): # one day not one days
                    array.append(f"{i+1}. {member.mention} has been in {ctx.guild.name} Discord for {zday} day and {zhour} hours.")
                    await message.edit(content=f"{message.content} \n {array[i]}")
                    i = i + 1
                    dormant = dormant + 1
                else:
                    array.append(f"{i+1}. {member.mention} has been in {ctx.guild.name} Discord for {zday} days and {zhour} hours.")
                    await message.edit(content=f"{message.content} \n {array[i]}")
                    i = i + 1
                    dormant = dormant + 1
            else:
                pass
        
        if (dormant == 0):
            await message.edit(content="There are no roleless users in the server that have stayed past their one week expiration date.")
                    
        
        print("Bouncing complete!")
    
    

    

def setup(bot):
    bot.add_cog(Bouncer(bot))