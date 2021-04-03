from discord import Embed


# Creates nice and simple embed templates for other files.
# dm_auto_embed: automatically sends DMs to user when they have tripped a filter
# dm_manual_embed: manual DM embeds with member argument


async def dm_auto_embed(
        message,
        title,
        body,
        footer,
        colour
):
    embed = Embed(
        title=title,
        description=f"{body}",
        color=colour,
    )

    embed.set_footer(text=footer)

    await message.author.send(embed=embed)


async def dm_manual_embed(
        member,
        title,
        body,
        footer,
        colour
):
    embed = Embed(
        title=title,
        description=f"{body}",
        color=colour,
    )

    embed.set_footer(text=footer)

    await member.send(embed=embed)


async def server_embed(
        channel,
        title,
        body,
        footer,
        colour
):

    embed = Embed(
        title=title,
        description=f"{body}",
        color=colour,
    )

    embed.set_footer(text=footer)

    await channel.send(embed=embed)






