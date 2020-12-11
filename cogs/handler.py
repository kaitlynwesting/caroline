import discord
import traceback
import sys
import random
from discord.ext import commands
from discord.ext.commands import MissingPermissions

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

    

def setup(bot):
    bot.add_cog(Handler(bot))