from utils import constants, embed_template


async def warn(
        ctx,
        infraction_member,
        infraction_reason
):

    public_message = f"📨 Applying **warning** to {infraction_member.mention}."

    private_message = f"**You were warned by {ctx.message.author}.**\n" \
                      f"{infraction_reason}\n " \

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

