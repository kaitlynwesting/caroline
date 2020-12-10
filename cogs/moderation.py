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

    # TEXT MUTE COMMAND
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, member: discord.Member):
        channel = discord.utils.get(ctx.guild.channels, name="logs") # god channel.id can be useful
    
        if get(ctx.guild.roles, name="Muted"):
            muted = get(ctx.guild.roles, name="Muted")
            await member.add_roles(muted)

            creator = get(ctx.guild.roles, name="Creator")
            await member.remove_roles(creator)
            await channel.send(f"{ctx.author.name} muted {member.mention}.") 
        else:
            await ctx.guild.create_role(name="Muted", colour=discord.Colour(0x2C2F33)) # make new role if not existing
            muted = get(ctx.guild.roles, name="Muted")
            await member.add_roles(muted)

            creator = get(ctx.guild.roles, name="Creator")
            await member.remove_roles(creator)
            await channel.send(f"A new muted role was created. {ctx.author.name} has muted {member.mention}.") # finally!

    # TEXT UNMUTE COMMAND
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, member: discord.Member):
        get(ctx.guild.roles, name="Muted")
        muted = get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muted)

        creator = get(ctx.guild.roles, name="Creator")
        await member.add_roles(creator)

        channel = discord.utils.get(ctx.guild.channels, name="logs") # god channel.id can be useful
        await channel.send(f"{ctx.author.name} unmuted {member.mention}.") 
    
    # KICK COMMAND
    @commands.command(name="kick")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        id = member.id
        if member == ctx.message.author:
            await ctx.channel.send("Are you daft? You can't kick yourself.")
            return
        if reason == None:
            reason = "Being an asshat"
            realreason = "No rationale provided (defaulted to preset message)"

        # dm the offending member the reason
        await member.send(f"You were kicked from {ctx.guild.name} for the following reason: {reason}.")
        await member.kick(reason=reason)
        for channel in member.guild.channels:
            if str(channel) == "logs":
                print(f"{realreason}")
                await channel.send(f"{ctx.author.name} kicked {member.mention} for the following cause: {realreason}") 
                break
    
    # BAN COMMAND
    @commands.command(name="ban")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        id = member.id
        if member == ctx.message.author:
            await ctx.channel.send("Are you daft? You can't ban yourself.")
            return
        if reason == None:
            reason = "Being an asshat"
            realreason = "No rationale provided (defaulted to preset message)"
        
        # dm the offending member the reason
        await member.send(f"You were banned from {ctx.guild.name} for the following reason: {reason}.")
        await member.ban(reason=reason)
        for channel in member.guild.channels:
            if str(channel) == "logs":
                print(f"{realreason}")
                await channel.send(f"{ctx.author.name} banned {member.mention} for the following cause: {realreason}") 
                break


    # UNBAN COMMAND
    @commands.command(name="unban")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user) #make the unban

                channel = discord.utils.get(ctx.guild.channels, name="logs") # god channel.id can be useful
                await channel.send(f"{ctx.author.name} unbanned {user.mention}.") # finally!
        
def setup(bot):
    bot.add_cog(Moderation(bot))