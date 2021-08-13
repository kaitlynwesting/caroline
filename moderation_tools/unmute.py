import discord
from utils import constants
from utils import embed_template


# A file for indefinite muting.
# Action: Auto text mutes for specified length of time.


async def unmute(
        ctx,
        pardoned_member
):
    muted = ctx.guild.get_role(constants.muted)

    public_message = (
        f"📨 Pardoned **mute** from {pardoned_member.mention}.",
    )

    private_message = (
        f"Your **mute** was pardoned by {ctx.message.author}.\n",
        f"You are free to continue talking in the server.",
    )

    # Public notification
    await ctx.channel.send(
        f"{''.join(public_message)}"
    )

    # Private notification
    await embed_template.dm_manual_embed(
        pardoned_member,
        f"Infraction pardoned from Photoshop Discord",
        f"{''.join(private_message)}",
        f"",
        constants.red
    )

    await pardoned_member.remove_roles(muted)
