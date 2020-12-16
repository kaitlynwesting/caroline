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
    @commands.command(name="warn")
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, member: discord.Member, *, reason): # reason is not None as warnings must be meaningful
        
        channel = discord.utils.get(ctx.guild.channels, name="logs") 

        if member.top_role < ctx.author.top_role:
            await member.send(f"You have received a warning from {ctx.guild.name} Discord for the following: {reason}")
            await channel.send(f"{ctx.author.name} issued a warning to {member.mention} for the following: {reason}")
        elif member.id == 785298572047417374:
            await ctx.send("You're not very bright, are you?")
        else:
            await ctx.send("How desperately you wish you could warn someone above or equal to your rank. But you can't. Boo, hoo.")

    # TEXT MUTE COMMAND
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, member: discord.Member):
        channel = discord.utils.get(ctx.guild.channels, name="logs") # god channel.id can be useful
        
        if member.top_role < ctx.author.top_role:
            if get(ctx.guild.roles, name="Muted"): # if such a role exists in the server

                muted = get(ctx.guild.roles, name="Muted")
                creator = get(ctx.guild.roles, name="Creator")

                if muted in member.roles: # check if they already have muted role
                    await channel.send(f"{member.mention} is already muted.")
                else:
                    await member.add_roles(muted)
                    await member.remove_roles(creator)

                    await member.send(f"You have been muted in the {ctx.guild.name} server.") # dm user
                    await channel.send(f"{ctx.author.name} muted {member.mention}.") 
            else:
                await ctx.guild.create_role(name="Muted", colour=discord.Colour(0x2C2F33)) # make new role if not existing
                muted = get(ctx.guild.roles, name="Muted")
                creator = get(ctx.guild.roles, name="Creator")
                
                await member.add_roles(muted)
                await member.remove_roles(creator)

                await member.send(f"You have been muted in the {ctx.guild.name} Discord.") # dm user
                await channel.send(f"A new muted role was created. {ctx.author.name} has muted {member.mention}.")
        elif member.id == 785298572047417374:
            await ctx.send("You're not very bright, are you?")
        else:
            await ctx.send("How desperately you wish you could mute someone above or equal to your rank. But you can't. Boo, hoo.")

    # TEXT UNMUTE COMMAND
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, member: discord.Member):
        get(ctx.guild.roles, name="Muted")
        muted = get(ctx.guild.roles, name="Muted")
        creator = get(ctx.guild.roles, name="Creator")
        channel = discord.utils.get(ctx.guild.channels, name="logs") # specify logging channel

        if muted in member.roles: 
            await member.remove_roles(muted)
            await member.add_roles(creator)
            
            await member.send(f"You have been unmuted in the {ctx.guild.name} Discord.") # dm user
            await channel.send(f"{ctx.author.name} unmuted {member.mention}.") 
        else:
            await ctx.send(f"{member.display_name} is not muted.")
    
    # KICK COMMAND
    @commands.command(name="kick")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        channel = discord.utils.get(ctx.guild.channels, name="logs") 

        if member == ctx.message.author:
            await ctx.channel.send("Are you daft? You can't kick yourself.")
            return
        
        if member.top_role < ctx.author.top_role:
            if reason == None:
                reason = "Being an asshat."
                await channel.send(f"{ctx.author.name} kicked {member.mention} for the following reason: No rationale provided (defaulted to preset message).")
            else: # successful kick.
                print(channel)
                await channel.send(f"{ctx.author.name} kicked {member.mention} for the following reason: {reason}")

                # dm the offending member the reason
                await member.send(f"You were kicked from {ctx.guild.name} Discord for the following reason: {reason}")
                await member.kick(reason=reason)
        elif member.id == 785298572047417374:
            await ctx.send("You're not very bright, are you?")
        else:
            await ctx.send("How desperately you wish you could kick someone above or equal to your rank. But you can't. Boo, hoo.")
            
    
    # BAN COMMAND
    @commands.command(name="ban")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        channel = discord.utils.get(ctx.guild.channels, name="logs")

        if member == ctx.message.author:
            await ctx.channel.send("Are you daft? You can't ban yourself.")
            return
        
        if member.top_role < ctx.author.top_role:
            if reason == None:
                reason = "Being an asshat."
                await channel.send(f"{ctx.author.name} banned {member.mention} for the following reason: No rationale provided (defaulted to preset message)")
            else:
                await channel.send(f"{ctx.author.name} banned {member.mention} for the following reason: {reason}")

            # dm the offending member the reason
            await member.send(f"You were banned from {ctx.guild.name} Discord for the following reason: {reason}")
            await member.ban(reason=reason)
        elif member.id == 785298572047417374:
            await ctx.send("You're not very bright, are you?")
        else:
            await ctx.send("How desperately you wish you could ban someone above or equal to your rank. But you can't. Boo, hoo.")
         
    # UNBAN COMMAND
    @commands.command(name="unban")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        state = False

        for ban_entry in banned_users:
            user = ban_entry.user
            

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user) #make the unban

                channel = discord.utils.get(ctx.guild.channels, name="logs") # god channel.id can be useful
                await channel.send(f"{ctx.author.name} unbanned {user.mention}.") # finally!
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