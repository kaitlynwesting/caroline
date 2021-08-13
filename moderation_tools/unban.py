import discord


# A file for unbanning.


async def unban(
        ctx,
        pardoned_member
):

    public_message = \
        f"📨 **Unbanned** {pardoned_member}."

    # Public notification of auto mute
    await ctx.channel.send(
        f"{public_message}"
    )

    pardoned_member = discord.Object(id=pardoned_member)
    await ctx.guild.unban(pardoned_member)

    # Add a section in front in the future to prevent dumbasses from trying to ban themselves
    # Add a section here in the future for preparing the logging file for logging actions
    # Add a section here in the future for documenting user info in a database
