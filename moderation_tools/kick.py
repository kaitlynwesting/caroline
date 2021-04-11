import discord
from utils import constants
from utils import embed_template


# A file for kicking.


async def kick(
        ctx,
        infraction_member: discord.Member,
        infraction_reason
):

    public_message = \
        f"📨 **Kicked** {infraction_member.mention} " \
        f"({infraction_reason})."

    private_message = \
        f"**You were kicked by {ctx.message.author}.**\n" \
        f"{infraction_reason}\n"

    await ctx.channel.send(
        f"{public_message}"
    )

    await embed_template.dm_manual_embed(
        infraction_member,
        f"Infraction received from Photoshop Discord",
        f"{private_message}",
        f"If you believe that there has been an error, please DM our Modmail bot.",
        constants.trouble_red
    )

    await infraction_member.kick(reason=infraction_reason)

    # Add a section in front in the future to prevent dumbasses from trying to ban themselves
    # Add a section here in the future for preparing the logging file for logging actions
    # Add a section here in the future for documenting user info in a database
