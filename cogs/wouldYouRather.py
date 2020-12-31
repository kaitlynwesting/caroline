import discord, requests
from discord.ext import commands

class WYR(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def wyr(self, ctx):
        question = requests.get('http://either.io/questions/next').json()['questions'][0]
        embed = discord.Embed(title="Would You Rather?", description=question['twitter_sentence'], color=0x00ff00)
        embed.add_field(name="A", value=question['option_1'])
        embed.add_field(name="B", value=question['option_2'])

        await ctx.send(embed=embed)
        
        
def setup(bot):
    bot.add_cog(WYR(bot))
