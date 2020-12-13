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
    async def bouncelist(self, ctx): 
        
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

            zday = z.days + 1
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
    

    # BOUNCES DORMANT ROLELESS USERS
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def bounce(self, ctx): # reason is not None as warnings must be meaningful
        
        creator = get(ctx.guild.roles, name="Creator")
        muted = get(ctx.guild.roles, name="Muted")
        channel = discord.utils.get(ctx.guild.channels, name="logs") 
        bots = get(ctx.guild.roles, name="Bots")

        i = 0
        namearray = []
        memberarray = []
        dormant = 0
        
        for member in ctx.guild.members:
            x = datetime.datetime.now()
            y = member.joined_at
            z = x - y

            zday = z.days + 1
            zhour = round(z.seconds/3600, 2)
            print(member)
            print(zday)
            
            if (zday > 7):
                if creator in member.roles or muted in member.roles or bots in member.roles:
                    pass
                else:
                    namearray.append(f"{i+1}. {member.mention}")
                    # await message.edit(content=f"{message.content} \n {namearray[i]}")
                    memberarray.append(f"{member.id}")
                    i = i + 1
                    dormant = dormant + 1
            else:
                pass
        

        if (dormant == 0):
            await ctx.send("There are no eligible members to eject.")
        else:
            ask = await ctx.send(f"Are you sure you would like to eject {dormant} member(s)?")
            
            def check(message):
                return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id
    
            msg = await self.bot.wait_for('message', check=check)
            
            if "yes" in msg.content.lower():
                await ctx.send("As you wish. Dormant members have been kicked and invites sent.") # actually

                for member in ctx.guild.members:
                    x = datetime.datetime.now()
                    y = member.joined_at
                    z = x - y

                    zday = z.days + 1
                    zhour = round(z.seconds/3600, 2)
                    print(member)
                    print(z)

                    # actual kicking area
                    if (zday > 7):
                        if creator in member.roles or muted in member.roles or bots in member.roles:
                            pass
                        else:
                            await member.kick(reason="Not accepting rules within one week")
                            await member.send(f"""You were kicked automatically from {ctx.guild.name} Discord, due to not accepting our rules for our verification period of one week. 
    If you'd like to join back, we welcome you! Use discord.gg/sx2P2KpU6G and type .accept.""")
                            i = i + 1
                    else:
                        pass
            else:
                await ctx.send("Coolio, okay.")

        print("Bouncing complete!")
    

def setup(bot):
    bot.add_cog(Bouncer(bot))