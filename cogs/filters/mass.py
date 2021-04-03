from discord.ext import commands
from moderation_tools import automute
from utils import filter_bypass


# A mass mentions filter.
# Listens for: @here and @everyone pings from non-exempt persons.
# Action: Removes message and mutes for 10 minutes.


class Mass(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(
            self,
            message
    ):

        if "@everyone" in message.content or "@here" in message.content:
            if message.guild is not None:

                can_bypass = await filter_bypass.bypass_check(message)  # Boolean to check if they are exempt

                if not can_bypass:
                    infraction_filter = "mass mentions"

                    infraction_description = (
                        # f"As much as I want to be snarky towards any individual who truly believed trying to tag 400+ ",
                        # f"people was going to get them instant service or something, I'll give you the benefit of the "
                        # f"doubt and assume it was a mistake.\n"
                        f"Because of the negative nature that people in the past have attempted to abuse ",
                        f"mass pings (as a vehicle for advertisements, spam, etc.), this filter was made to deter, as ",
                        f"well as remove, messages by those unwanted visitors.\n",
                        f"As a future precaution, please refrain from mass pings."
                    )

                    await automute.automute(
                        message,
                        f"{infraction_filter}",
                        f"{''.join(infraction_description)}",
                        10,
                    )


def setup(bot):
    bot.add_cog(Mass(bot))
