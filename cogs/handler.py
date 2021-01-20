import discord
import traceback
import sys
import random
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands import CommandNotFound
from discord.utils import get

class Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        num = str((random.randint(2, 10)))

        # INSUFFICIENT PARAMETERS
        if isinstance(error, commands.MissingRequiredArgument):
            mra = ["Think you're missing an argument or " + num + f", {ctx.message.author.display_name}.", 
                    "Insufficient arguments.",
                    f"{ctx.message.author.display_name}, mate, you need more parameters."]
            await ctx.send(random.choice(mra))
        
        # INSUFFICIENT PERMISSIONS
        if isinstance(error, commands.MissingPermissions):
            #await ctx.send("You simply have less value.")
            await ctx.send("You can't. Why?", file=discord.File("./media/image1.jpg"))
        
        # CAN'T FIND COMMAND
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Couldn't find that command, sorry.")
        
        # ON COOLDOWN
        if isinstance(error,commands.CommandOnCooldown):
            mod = get(ctx.guild.roles, name="Moderator")

            if mod in ctx.author.roles:
                pass
            
            else:
                await ctx.send("You're on cooldown.")
        
        # BAD ARGUMENTS
        if isinstance(error,commands.ArgumentParsingError):
            await ctx.send("Bleh, smelled a bad argument.")

    

def setup(bot):
    bot.add_cog(Handler(bot))