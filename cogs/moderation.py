import discord
from discord.ext import commands
from discord.utils import get

import traceback
import sys
import random

# COG FOR MODERATION PURPOSES.

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # WARN COMMAND
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, member: discord.Member, reason): # reason is not None as warnings must be meaningful
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
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, member: discord.Member):
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

                await ctx.send(f"📨 Applied **mute** to {member.mention}.")
                await member.send(f"You have been **muted** indefinitely in the {ctx.guild.name} Discord.") # dm user
                await channel.send(f"**[MODERATION]** {ctx.author.name} muted {member.mention}.") 


    # TEXT UNMUTE COMMAND
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, member: discord.Member):
        muted = get(ctx.guild.roles, name="Muted")
        creator = get(ctx.guild.roles, name="Creator")
        channel = discord.utils.get(ctx.guild.channels, name="logs") 

        if muted in member.roles: 
            await member.remove_roles(muted)
            await member.add_roles(creator)
            
            await ctx.send(f"Done! {member.mention} has been **unmuted** now.")
            await member.send(f"You have been unmuted in the {ctx.guild.name} Discord.") # dm user
            await channel.send(f"**[MODERATION]** {ctx.author.name} unmuted {member.mention}.") 

        else:
            await ctx.send(f"{member.display_name} is not muted.")
    

    # KICK COMMAND
    @commands.command(name="kick")
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
            await message.author.send(f"You have been **kicked** from {message.guild.name} Discord for the following: {reason}")
            await member.kick(reason=reason)
    
    # BAN COMMAND
    @commands.command(name="ban")
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
            await message.author.send(f"You have been **banned** permanently from {message.guild.name} Discord for the following: {reason}")
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

                await channel.send(f"**[MODERATION]** {ctx.author.name} unbanned {user.mention}.") # finally!
                state = True
            else:
                pass
        
        if state == False:
            await ctx.send("Are you sure they're on the banlist? Couldn't find anyone matching that name.")
        else:
            pass

    # TEMPBAN (WIP)
    """ @client.command()
    async def tempban(ctx, member: discord.Member, duration:int, *, reason=None):
        
        
        await member.send(f"You were banned from {ctx.guild.name} for the following reason: {reason}.")
        await member.ban(reason=reason)
        print(reason)
        await ctx.send(f"{ctx.author.name} tempbanned {member.mention} for a duration of {duration} minutes, for the following cause:  {realreason}")   """

def setup(bot):
    bot.add_cog(Moderation(bot))
