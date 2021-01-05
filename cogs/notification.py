import discord
import traceback
import sys
import random
from discord.ext import commands
from discord.utils import get

class Notification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # POLL FOR LIVESTREAMING NOTIFICATION
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = discord.utils.get(message.guild.channels, name="moderator-chat")
        a = discord.utils.get(message.guild.channels, name="announcements")

        fin = open("cogs/texts/voters.txt", "r")

        voters = fin.readlines()
        x = str(message.author)
        y = "\n"
        z = x + y

        if z in voters:
            pass
        elif message.author.bot == True:
            pass
        else:
            fout = open("cogs/texts/voters.txt", "a")

            embed=discord.Embed(color=0x349feb)

            embed.set_author(name=f"Hi there, {message.author.display_name}!", icon_url=message.author.avatar_url)
            embed.add_field(name="The friendly neighbourhood bot (and the community) seeks your opinion:", value=f"""We don't know if you've seen our latest {a.mention}, but we have an exciting poll for you. If you haven't voted yet, we entreat you!""", inline=False)
            embed.set_footer(text="Alright, alright, I'll stop pestering you. If you've been a dutiful voter, thanks ;)")
            await message.channel.send(embed=embed)

            fout.write(f"{message.author}\n") 
            return
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! The latency is {round(self.bot.latency, 3)} milliseconds.")
        

def setup(bot):
    bot.add_cog(Notification(bot))