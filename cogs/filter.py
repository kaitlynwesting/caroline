import discord
import traceback
import sys
import random
from discord.ext import commands
from discord.utils import get

class Filter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # NO ADVERTISING
    @commands.Cog.listener()
    async def on_message(self, message):
        mod = get(message.guild.roles, name="Moderator")

        if "discord.gg" in str(message.content):
        
            if mod in message.author.roles:
                pass
            elif message.author.id == 785298572047417374: # Lydia id lol
                pass
            elif str(message.content) == "https://discord.gg/XttKUrsTxb" or "https://discord.gg/GBmSvDTf9G":
                pass
            else:
                await message.channel.purge(limit=1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True)
    
    @commands.Cog.listener()
    async def on_message(self, message):

        #await channel.send(f"**[MODERATION]** {message.author.mention} was muted (tried to pull an everyone ping).")
        if "@everyone" in message.content or "@here" in message.content:

            mod = get(message.guild.roles, name="Moderator")
            muted = get(message.guild.roles, name="Muted")
            
            if mod in message.author.roles:
                pass
            else:
                for role in message.author.roles:
                        try:
                            await message.author.remove_roles(role)
                        except:
                            pass 
                    
                await message.author.add_roles(muted)

                channel = get(message.guild.channels, name="logs")
                await channel.send(f"**[MODERATION]** {message.author.mention} was muted (tried to pull a mass ping).")
                await message.channel.send(f"📨 Applied **auto-mute** to {message.author.mention} (infraction: `attempting mass ping`).")
                await message.author.send(f"You have been **auto-muted** in {message.guild.name} Discord, for thinking you're important enough to disturb everyone's peace.") 

def setup(bot):
    bot.add_cog(Filter(bot))