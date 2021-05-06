from discord.ext import commands
from utils import constants


class Voting(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        context_channel = self.bot.get_channel(payload.channel_id)
        context_message = await context_channel.fetch_message(payload.message_id)
        context_emoji = str(payload.emoji)

        voting_emoji = "<:blobFingerGuns:833076453050023987>"
        voted_times = 0

        if context_channel.id == constants.events:

            if context_emoji == voting_emoji:

                async for message in context_channel.history(limit=25):

                    if 'Challenge Number' in message.content:

                        async for submission in context_channel.history(after=message):

                            # Looks at each reaction for each submission after event marker
                            for reaction in submission.reactions:

                                # Looks at each user for each reaction
                                async for user in reaction.users():

                                    if user == payload.member and str(reaction) == voting_emoji:

                                        voted_times += 1

                                        if voted_times > 1:
                                            await context_message.remove_reaction(reaction, user)
                                            reminder_message = \
                                                await context_channel.send(f"**No voting more than once, "
                                                                           f"{user.mention}!** If you wish to "
                                                                           f"vote for a different person, remove your "
                                                                           f"previous vote first.")
                                            await reminder_message.delete(delay=3)

                                            return

                                    if user == payload.member and user == submission.author:
                                        await context_message.remove_reaction(reaction, user)
                                        reminder_message = \
                                            await context_channel.send(f"**Shame, {user.mention}, you tried to vote"
                                                                       f"for yourself!** Self voting is not allowed.")
                                        await reminder_message.delete(delay=3)

                                        return

                        return


def setup(bot):
    bot.add_cog(Voting(bot))
