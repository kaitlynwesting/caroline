import asyncio
import discord
from discord.ext import commands
from discord.utils import get

async def infraction_notification(message, rule, time: int):
    await message.channel.send(f"📨 Applying **auto tempmute** to {message.author.mention} for {time} minutes (rule: `{rule}`).")

# EMBED DM FOR AUTOMATIC TEMPMUTES.
async def infraction_auto_embed(message, rule, description):
    
    embed=discord.Embed (
        title = f"Infraction received from Photoshop Discord", 
        color=0xeb4034, 
        )

    embed.add_field(
        name=f"You were automatically tempmuted due to our `{rule}` filter.", 
        value=description, 
        inline=False
        )
    
    embed.set_footer(text="If you believe there has been a mistake, please contact our Modmail bot.")

    await message.author.send(embed=embed)


# EMBED DM FOR EXPIRED TEMPMUTE (FOR MUTES AND SUCH).
async def infraction_auto_over_embed(message, infraction=None):
    
    embed=discord.Embed (
        title = f"Infraction timeout from Photoshop Discord", 
        color=0xeb4034, 
        )

    embed.add_field(
        name=f"Your tempmute has timed out.", 
        value=f"You are now free to continue chatting in Photoshop Discord. Be mindful of our <#777237462904209429> when you speak again.", 
        inline=False
        )

    await message.author.send(embed=embed)

# A MUTE FUNCTION
async def infraction_mute(message):
    muted = get(message.guild.roles, name = "Muted")
    announcements = get(message.guild.roles, name = "Announcements")

    if muted in message.author.roles: 
        await message.channel.send(f"{message.author.mention} is already muted.")
    else:
        for role in message.author.roles:
            if role is not announcements:
                try:    
                    await message.author.remove_roles(role)
                except:
                    pass
        await message.author.add_roles(muted)


async def infraction_tempmute(message, time: int):
    creator = get(message.guild.roles, name = "Creator")
    muted = get(message.guild.roles, name = "Muted")
    announcements = get(message.guild.roles, name = "Announcements")

    omitted_roles = [announcements]

    if muted in message.author.roles: 
        await message.channel.send(f"{message.author.mention} is already muted.")
    else:
        for role in message.author.roles:
            if role not in omitted_roles:
                try:    
                    await message.author.remove_roles(role)
                except:
                    pass
        await message.author.add_roles(muted)

        await asyncio.sleep(time * 60)
    
        await message.author.remove_roles(muted)
        await message.author.add_roles(creator)
        await infraction_auto_over_embed(message)
    




