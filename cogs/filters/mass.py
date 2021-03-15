from discord.ext import commands
from discord.utils import get

from ..utils import infraction
from ..utils import filter_bypass

# A mass mentions filter which aims to detect mass pings and shut up weirdos


class Mass(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if "@everyone" in message.content or "@here" in message.content:

            can_bypass = await filter_bypass.bypass_check(message) # Boolean - are they exempt from filter?
            print(message.author, 'CAN BYPASS IS...', can_bypass)

            if can_bypass == False:

                punishment_time = 10  # Time, in minutes, of automute time

                with open('cogs/texts/infraction.txt', 'r') as f:
                    rules = f.readlines()

                rule1 = (rules[2])[0:-1]
                rule2 = (rules[3])[0:-1]
                rule3 = ((rules[14])[0:-1]).replace("punishment", str(punishment_time))
 
                infraction_description = ("Apparently, you deemed yourself important enough to disturb ~400 people. "
                                          f"{rule3}. {rules[13]}")
        
                await infraction.infraction_notification(message, "mass mentions", punishment_time)
                await infraction.infraction_auto_embed(message, "mass mentions", infraction_description)
                await infraction.infraction_tempmute(message, punishment_time)


def setup(bot):
    bot.add_cog(Mass(bot))
