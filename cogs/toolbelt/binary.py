import discord
import traceback
import sys
import random
import datetime
from discord.ext import commands

class Maths(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def binary(self, ctx, msg, *, code): 
        
        if (msg == "decode"):
            a_binary_string = str(code)


            binary_values = a_binary_string.split()

            ascii_string = ""

            for binary_value in binary_values:

                an_integer = int(binary_value, 2)
                ascii_character = chr(an_integer)
                ascii_string += ascii_character

            await ctx.send(f"Your decoded binary is: {ascii_string}")
        
        elif (msg == "encode"):
            string = str(code)
  
            
            # using join() + ord() + format() 
            # Converting String to binary 
            res = ' '.join(format(ord(i), 'b') for i in string) 
            
            # printing result  
            await ctx.send(f"Your encoded binary is: {str(res)}") 

    

def setup(bot):
    bot.add_cog(Maths(bot))