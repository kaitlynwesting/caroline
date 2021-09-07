import discord
from cogs.utils import constants, embed_template


# A file for banning.
# Action: permanently bans a user.


async def ban(
        ctx,
        infraction_member: discord.Member,
        infraction_reason
):

    public_message = \
        f"📨 Permanently **banned** {infraction_member.mention} " \
        f"({infraction_reason})."

    private_message = \
        f"**You were banned by {ctx.message.author}.**\n" \
        f"{infraction_reason}\n"

    # Public notification
    await ctx.channel.send(
        f"{public_message}"
    )

    # Private notification
    try:
        await embed_template.dm_manual_embed(
            infraction_member,
            f"Infraction received from Photoshop Discord",
            f"{private_message}",
            f"This ban is permanent and will not be revoked.",
            constants.red
        )
    except discord.errors.Forbidden:
        print(f"Tried to DM {infraction_member} before banning, but their DMs were disabled. Moving on.")

    await infraction_member.ban(reason=infraction_reason)

    # Add a section in front in the future to prevent people from trying to ban themselves
    # Add a section here in the future for preparing the logging file for logging actions
    # Add a section here in the future for documenting user info in a database
