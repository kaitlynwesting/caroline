import discord
import traceback
import sys
import random
from discord.ext import commands



class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #KICK COMMAND
    @commands.command(name="boot")
    @commands.has_permissions(ban_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        id = member.id
        if member == ctx.message.author:
            await ctx.channel.send("Are you daft? You can't ban yourself.")
            return
        if reason == None:
            reason = "Being an asshat"
            realreason = "No rationale provided (defaulted to preset message)"
        await member.send(f"You were kicked from {ctx.guild.name} for the following reason: {reason}.")
        await member.kick(reason=reason)
        for channel in member.guild.channels:
            if str(channel) == "logs": # channel check here
                await channel.send(f"{ctx.author.name} kicked {member.mention} for the following cause: {realreason}.") 
                print("reason is", reason, id)
    
    # BAN COMMAND
    @commands.command(name="bam")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        id = member.id
        if member == ctx.message.author:
            await ctx.channel.send("Are you daft? You can't ban yourself.")
            return
        if reason == None:
            reason = "Being an asshat"
            realreason = "No rationale provided (defaulted to preset message)"
        await member.send(f"You were banned from {ctx.guild.name} for the following reason: {reason}.")
        await member.ban(reason=reason)
        for channel in member.guild.channels:
            if str(channel) == "logs": # channel check here
                await channel.send(f"{ctx.author.name} banned {member.mention} for the following cause: {realreason}.") 
                print("reason is", reason, id)

def setup(bot):
    bot.add_cog(Moderation(bot))