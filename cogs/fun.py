import discord, requests, linecache, cogs.utils.constants
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wyr(self, ctx):
        question = requests.get('http://either.io/questions/next').json()['questions'][0]
        embed = discord.Embed(title="Would You Rather?", description=question['twitter_sentence'], color=0x00ff00)
        embed.add_field(name="A", value=question['option_1'])
        embed.add_field(name="B", value=question['option_2'])

        await ctx.send(embed=embed)

    
    @commands.command()
    async def question(self, ctx):
        questionNumber = 3
        questionText = linecache.getline('media/questions.txt', questionNumber)

        embed = discord.Embed.from_dict({'title': f'Question #{questionNumber}',
                                     'description': questionText,
                                     'color': cogs.utils.constants.blurple
                                     })

        await ctx.send(embed=embed)
        
        
async def setup(bot):
    await bot.add_cog(Fun(bot))
