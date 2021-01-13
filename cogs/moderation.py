import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime, timezone, timedelta
import pytz

import asyncio
import traceback
import sys
import random

# COG FOR MODERATION PURPOSES.

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # WARN COMMAND
    @commands.command(aliases=["w"])
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, member: discord.Member, *, reason): # reason is not None as warnings must be meaningful
        channel = discord.utils.get(ctx.guild.channels, name="logs") 

        if member.id == 785298572047417374:
            await ctx.send("You're not very bright, are you?")

        elif member == ctx.message.author: # Stop muting yourself
            await ctx.channel.send("Are you daft? You can't mute yourself.")

        elif member.top_role >= ctx.author.top_role and ctx.author.id != 669977303584866365:
            await ctx.send("How desperately you wish you could warn someone above or equal to your rank. But you can't. Boo, hoo.")

        else:
            await ctx.send(f"📨 Delivered **warning** to {member.mention} ({reason}).")
            await member.send(f"You have received a **warning** from {ctx.guild.name} Discord for the following: {reason}")
            await channel.send(f"**[MODERATION]** {ctx.author.name} issued a warning to {member.mention} for the following: {reason}")


    # TEXT MUTE COMMAND
    @commands.command(aliases=["m"])
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        channel = discord.utils.get(ctx.guild.channels, name="logs")
        muted = get(ctx.guild.roles, name="Muted")

        if member.id == 785298572047417374: # Lydia id lol
            await ctx.send("You're not very bright, are you?")

        elif member == ctx.message.author: # Stop muting yourself
            await ctx.channel.send("Are you daft? You can't mute yourself.")

        elif member.top_role >= ctx.author.top_role and ctx.author.id != 669977303584866365: # Why would you try this
            await ctx.send("How desperately you wish you could mute someone above or equal to your rank. But you can't. Boo, hoo.")

        else:
            if muted in member.roles: # Do you already have muted role
                await ctx.send(f"{member.mention} is already muted.")
            else:
                for role in member.roles:
                    try:
                        await member.remove_roles(role)
                    except:
                        pass 
                
                await member.add_roles(muted)
                
                if reason == None:
                    reason = "Being an asshat."
                    await channel.send(f"**[MODERATION]** {ctx.author.name} muted {member.mention} for the following reason: No rationale provided (defaulted to preset message).")

                else: 
                    await channel.send(f"**[MODERATION]** {ctx.author.name} muted {member.mention} for the following reason: {reason}")

                await ctx.send(f"📨 Applied **mute** to {member.mention} indefinitely.")
                await member.send(f"You have been **muted** indefinitely in {ctx.guild.name} Discord for the following: {reason}")


    # TEMPMUTE (WIP)
    @commands.command(aliases=["tempm", "tm"])
    async def tempmute(self, ctx, member: discord.Member, duration, *, reason=None):
        channel = discord.utils.get(ctx.guild.channels, name="logs")
        muted = get(ctx.guild.roles, name="Muted")
        creator = get(ctx.guild.roles, name="Creator")
        
        timeConvert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        timeStringSingular = {"s": "second", "m": "minute", "h": "hour", "d": "day"}
        timeStringPlural = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}
        
        def convert(time):
            try:
                return int(time[:-1]) * timeConvert[time[-1]] # in seconds
            except:
                return time # in seconds
        
        def timeToString(time):
            if time[:1] == "1" and len(time) == 2:
                try:
                    return str(f"{time[:-1]} {timeStringSingular[time[-1]]}") # in seconds
                except:
                    return
            else:
                try:
                    return str(f"{time[:-1]} {timeStringPlural[time[-1]]}") # in seconds
                except:
                    return
        
        sleepTime = convert(duration) # convert everything to seconds!
        displayTime = timeToString(str(duration))
        
        nowTime = datetime.now(tz=timezone.utc)
        muteTime = timedelta(seconds=sleepTime)
        finishTime = nowTime + muteTime
        
        muteTime = str(muteTime)
        finishTime = str(finishTime)
        finishTime = finishTime[:-13]

        if member.id == 785298572047417374: # Lydia id lol
            await ctx.send("You're not very bright, are you?")

        elif member == ctx.message.author: # Stop muting yourself
            await ctx.channel.send("Are you daft? You can't mute yourself.")

        elif member.top_role >= ctx.author.top_role and ctx.author.id != 669977303584866365: # Why would you try this
            await ctx.send("How desperately you wish you could mute someone above or equal to your rank. But you can't. Boo, hoo.")

        else:
            if muted in member.roles: # Do you already have muted role
                await ctx.send(f"{member.mention} is already muted.")
            else:
                for role in member.roles:
                    try:
                        await member.remove_roles(role)
                    except:
                        pass 
                
                await member.add_roles(muted)
                
                if reason == None:
                    reason = "Being an asshat."
                    await channel.send(f"**[MODERATION]** {ctx.author.name} **tempmuted** {member.mention} for the following reason: No rationale provided (defaulted to preset message). The tempmute will last until {finishTime} ({displayTime}) UTC.")

                else: 
                    await channel.send(f"**[MODERATION]** {ctx.author.name} **tempmuted** {member.mention} for the following reason: {reason}. The tempmute will last until {finishTime} ({displayTime}) UTC.")
                
                await ctx.send(f"📨 Applying **tempmute** to {member.mention} until {finishTime} ({displayTime}) UTC.")
                await member.send(f"You have been **tempmuted** in {ctx.guild.name} Discord for the following: {reason}. You will be unmuted automtically at {finishTime} UTC.")

                await asyncio.sleep(sleepTime) # wait and snooze

                if muted in member.roles: 
                    await member.remove_roles(muted)
                    await member.add_roles(creator)
                    
                    await member.send(f"You have been **unmuted** automatically in {ctx.guild.name} Discord.") # dm user
                    await channel.send(f"**[MODERATION]** 📨 {member.mention} has been automatically **unmuted** now.") 
        

    # TEXT UNMUTE COMMAND
    @commands.command(aliases=["um"])
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, member: discord.Member):
        channel = discord.utils.get(ctx.guild.channels, name="logs") 
        muted = get(ctx.guild.roles, name="Muted")
        creator = get(ctx.guild.roles, name="Creator")

        if muted in member.roles: 
            await member.remove_roles(muted)
            await member.add_roles(creator)
            
            await ctx.send(f"📨 Done! {member.mention} has been **unmuted** now.")
            await member.send(f"You have been **unmuted** in {ctx.guild.name} Discord.") # dm user
            await channel.send(f"**[MODERATION]** {ctx.author.name} unmuted {member.mention}.") 

        else:
            await ctx.send(f"{member.display_name} is not muted.")
    

    # KICK COMMAND
    @commands.command(aliases=["k"])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        channel = discord.utils.get(ctx.guild.channels, name="logs") 
        
        if member.id == 785298572047417374:
            await ctx.send("You're not very bright, are you?")

        elif member == ctx.message.author:
            await ctx.channel.send("Are you daft? You can't kick yourself.")

        elif member.top_role >= ctx.author.top_role and ctx.author.id != 669977303584866365:
            await ctx.send("How desperately you wish you could kick someone above or equal to your rank. But you can't. Boo, hoo.")

        else:
            if reason == None:
                reason = "Being an asshat."
                await channel.send(f"**[MODERATION]** {ctx.author.name} kicked {member.mention} for the following reason: No rationale provided (defaulted to preset message).")

            else: # successful kick.
                await channel.send(f"**[MODERATION]** {ctx.author.name} kicked {member.mention} for the following reason: {reason}")

            await ctx.send(f"📨 **Kicked** {member.mention} ({reason}).")
            await member.send(f"You have been **kicked** from {ctx.guild.name} Discord for the following: {reason}")
            await member.kick(reason=reason)
    
    # BAN COMMAND
    @commands.command(aliases=["b"])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        channel = discord.utils.get(ctx.guild.channels, name="logs") 
        
        if member.id == 785298572047417374:
            await ctx.send("You're not very bright, are you?")

        elif member == ctx.message.author:
            await ctx.channel.send("Are you daft? You can't ban yourself.")

        elif member.top_role >= ctx.author.top_role and ctx.author.id != 669977303584866365:
            await ctx.send("How desperately you wish you could ban someone above or equal to your rank. But you can't. Boo, hoo.")

        else:
            if reason == None:
                reason = "Being an asshat."
                await channel.send(f"**[MODERATION]** {ctx.author.name} banned {member.mention} for the following reason: No rationale provided (defaulted to preset message).")

            else: 
                print(channel)
                await channel.send(f"**[MODERATION]** {ctx.author.name} banned {member.mention} for the following reason: {reason}")

            await ctx.send(f"📨 Permanently **banned** {member.mention} ({reason}).")
            print(member)
            await member.send(f"You have been **banned** permanently from {ctx.guild.name} Discord for the following: {reason}")
            await member.ban(reason=reason)
         
    
    # UNBAN COMMAND
    @commands.command(name="unban")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        channel = discord.utils.get(ctx.guild.channels, name="logs")
        bannedUsers = await ctx.guild.bans()
        memberName, memberDiscriminator = member.split("#")
        state = False

        for banEntry in bannedUsers:
            user = banEntry.user
            
            if (user.name, user.discriminator) == (memberName, memberDiscriminator):
                await ctx.guild.unban(user) #make the unban
                
                await ctx.send(f"📨 Gotcha, {user.mention} has been **unbanned**.")
                await channel.send(f"**[MODERATION]** {ctx.author.name} unbanned {user.mention}.") # finally!
                state = True
            else:
                pass
        
        if state == False:
            await ctx.send("Are you sure they're on the banlist? Couldn't find anyone matching that name.")
        else:
            pass

        

def setup(bot):
    bot.add_cog(Moderation(bot))
