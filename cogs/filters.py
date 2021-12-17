from discord.ext import commands
from moderation_tools import automute
from cogs.utils import constants, filter_bypass


# A server advertisements filter.
# Listens for: external Discord and Disboard invites from non-exempt persons.
# Action: Removes message and mutes for 30 minutes.


class Ad(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ANTI-ADVERTISING FILTER
    @commands.Cog.listener()
    async def on_message(
            self,
            message
    ):
        if message.guild is not None:

            splitted = message.content.split()

            # Examine each message for discord.gg links
            message_invites = [s for s in splitted if "discord.gg" in s]

            # Replace useless https:// prefix for matching.
            message_invites = [i.replace("https://", "") for i in message_invites]

            # Fetch list of all active invites and our disboard page, and concat into a list of server invites.
            server_invite_raw = await message.guild.invites()
            server_invites = [i.url for i in server_invite_raw]
            server_invites = [i.replace("https://", "") for i in server_invites]

            # If invite(s) have been detected in the user's message...
            if len(message_invites) > 0:
                is_advertising = not all(i in server_invites for i in message_invites)

                if is_advertising is True:
                    can_bypass = await filter_bypass.bypass_check(message)

                    if not can_bypass:
                        await message.channel.purge(limit=1)

                        infraction_filter = "advertising"

                        infraction_description = (
                            f"Are you sure you even read the <#{constants.rules}>?\n",
                            f"Please post your lame Discord server links elsewhere, or better yet, don't post at all—",
                            f"most people don't appreciate pollution in their communities."
                        )

                        await automute.automute(
                            message,
                            f"{infraction_filter}",
                            f"{''.join(infraction_description)}",
                            30,
                        )


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
    bot.add_cog(Ad(bot))
    bot.add_cog(Mass(bot))