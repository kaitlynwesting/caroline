import asyncio
from utils import constants, embed_template, time_converter
from utils.constants import events

# Temporary mute function.
# If the muting period is not specified, the default is 7d.


async def mute(
        ctx,
        infraction_member,
        infraction_time,
        infraction_reason
):
    muted = ctx.guild.get_role(constants.muted)

    infraction_time_int = time_converter.time_to_int(infraction_time)
    infraction_time_string = time_converter.time_to_string(infraction_time)
    infraction_time_date = time_converter.time_to_date(infraction_time)

    public_message = (
        f"📨 Applying **mute** to {infraction_member.mention} ",
        f"until {infraction_time_date} UTC ({infraction_time_string})."
    )

    private_message = (
        f"**You were muted by {ctx.message.author}.**\n",
        f"{infraction_reason}\n",
        f"**You will be muted until {infraction_time_date} UTC ({infraction_time_string})**."
    )

    # Public notification of auto mute
    await ctx.channel.send(
        f"{''.join(public_message)}"
    )

    # Private notification of mute
    await embed_template.dm_manual_embed(
        infraction_member,
        f"Infraction received from Photoshop Discord",
        f"{''.join(private_message)}",
        f"If you believe that there has been an error, please DM our Modmail bot.",
        constants.red
    )

    await infraction_member.add_roles(muted)

    await asyncio.sleep(infraction_time_int)

    if muted in infraction_member.roles:

        await infraction_member.remove_roles(muted)

        await embed_template.dm_manual_embed(
            infraction_member,
            f"Infraction expired from Photoshop Discord",
            f"Your mute has expired.\n"
            f"You are free to continue talking in the server.",
            "",
            constants.red
        )
