# Work with Python 3.6
import discord
from discord.ext import commands
from discord.utils import get

import os
import settings

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = discord.ext.commands.Bot(command_prefix = settings.prefix, intents = intents)
# channel = client.get_channel(int(690290724994023519))
print("Loading discord.py version", discord.__version__, ", starting...")

# base test commands

@client.event # this is a listener that listens for messages
async def on_message(message):
	if message.content == "hello":
		await message.channel.send("pies are better than cakes. change my mind.")

	await client.process_commands(message) #WAIT FOR BOT TO PROCESS COMMANDS BEFORE LISTENER

@client.command()
async def ping(ctx): #no arguments
    channel = client.get_channel(769410662081495090) # replace id with the welcome channel's id
    await channel.send("pong has arrived!") 

# tempban (experimental)
@client.command()
async def tempban(ctx, member: discord.Member, duration:int, *, reason=None):
    with open('tempbans.txt','a') as file:
        file.write(f"{member.name}#{member.discriminator}#{duration}")
        file.write("\n")
        print("Logged a tempban.")
    
    await member.send(f"You were banned from {ctx.guild.name} for the following reason: {reason}.")
    await member.ban(reason=reason)
    print(reason)
    await ctx.send(f"{ctx.author.name} tempbanned {member.mention} for a duration of {duration} minutes, for the following cause:  {realreason}")  


# bot loading messages on ready
@client.event
async def on_ready():
    print("I am ready!")

    # set the now playing status
    if settings.nowplaying:
            print("Setting now playing game...", flush= True)
            await client.change_presence(activity=discord.Game(name=settings.nowplaying))
    
    # loader for cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try: 
                client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Failed to load {filename}")
    print("-----")

    # vanity print messages
    print("Logged in as:", client.user.name)
    print("My id is:", client.user.id)
    print("My prefix is:", settings.prefix)
    print('-----')

# client.load_extension("cogs.greetings")

client.run(settings.token)
