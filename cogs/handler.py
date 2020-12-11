import discord
import traceback
import sys
import random
from discord.ext import commands

class Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # INSUFFICIENT PARAMETERS
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        num = str((random.randint(2, 10)))
        if isinstance(error, commands.MissingRequiredArgument):
            mra = ["Think you're missing an argument or " + num + f", {ctx.message.author.display_name}.", 
                    "Insufficient arguments, pal.",
                    f"{ctx.message.author.display_name}, mate, you need more parameters."]
            await ctx.send(random.choice(mra))

    # INSUFFICIENT PERMISSIONS
    @commands.Cog.listener()
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You just have less value.")

def setup(bot):
    bot.add_cog(Handler(bot))