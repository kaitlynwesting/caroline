import asyncio
from utils import constants
from utils import embed_template


# A file for automatic muting.
# Immediately follows, and is only expected, to work with filters.
# Action: Auto text mutes for specified length of time.

async def automute(
        message,
        infraction_filter,
        infraction_description,
        infraction_time
):
    muted = message.guild.get_role(constants.muted)

    public_message = (
        f"📨 Applying **auto tempmute** to {message.author.mention} ",
        f"for {infraction_time} minutes (rule: `{infraction_filter}`) "
    )

    private_message = (
        f"**You were automatically tempmuted due to our `{infraction_filter}` filter.**\n",
        f"{infraction_description}\n",
        f"**You will be muted for `{infraction_time} minutes`, starting from the time of this message.**"
    )

    # Public notification of auto mute
    await message.channel.send(
        f"{''.join(public_message)}"
    )

    # Private notification of auto mute
    await embed_template.dm_auto_embed(
        message,
        f"Infraction received from Photoshop Discord",
        f"{''.join(private_message)}",
        f"If you believe that there has been an error, please DM our Modmail bot.",
        constants.red
    )

    await message.author.add_roles(muted)

    await asyncio.sleep(infraction_time * 60)

    if muted in message.author.roles:
        await message.author.remove_roles(muted)

        await embed_template.dm_auto_embed(
            message,
            f"Infraction expired from Photoshop Discord",
            f"Your mute has expired. You are free to continue talking in the server.",
            "",
            constants.red
        )
