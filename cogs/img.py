# stolen from https://github.com/PoldekPL/SauceBot/blob/master/bot.py
import discord
from discord.ext import commands
import asyncio
import random
import time
import sys
import traceback
import os
import os.path
import subprocess
import functools
import re
import pickle
from urllib import parse


def getLogFormattedTime():
    timestamp_now = time.gmtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", timestamp_now)

class SauceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="all", aliases=["a"])
    async def sauceAll(self, ctx):
        await self.replyLinks(ctx, saucenao=True, google=True, tineye=True, iqdb=True, yandex=True)

    # a majestic function name, I know
    @commands.command(name="saucenao", aliases=["sauce", "s", "e621", "e"])
    async def sauceSauce(self, ctx):
        await self.replyLinks(ctx, saucenao=True)

    @commands.command(name="google", aliases=["g"])
    async def sauceGoogle(self, ctx):
        await self.replyLinks(ctx, google=True)

    @commands.command(name="tineye", aliases=["t"])
    async def sauceTineye(self, ctx):
        await self.replyLinks(ctx, tineye=True)

    @commands.command(name="iqdb", aliases=["i"])
    async def sauceIQDB(self, ctx):
        await self.replyLinks(ctx, iqdb=True)

    @commands.command(name="yandex", aliases=["y"])
    async def sauceYandex(self, ctx):
        await self.replyLinks(ctx, yandex=True)

    async def replyLinks(self, ctx, saucenao=False, google=False, tineye=False, iqdb=False, yandex=False):
        # analyze the message to decide what's the user's intent
        result = self.analyzeCommand(ctx)

        # let's build a list of urls to generate links with
        urls = []
        if result == "file":
            # user attached file(s), get url(s)
            urls = self.getMessageAttachmentURLs(ctx.message)

        elif result == "link":
            # user has sent a string, assume it's a valin picture url
            link = ctx.message.content.replace(ctx.prefix + ctx.invoked_with, "").strip()
            urls = [link]

        elif result == "discord link":
            # user linked a discord message, extract server, channel and message ids
            ids = re.findall(r"\d+", ctx.message.content, re.I)

            # get the server
            linked_guild = self.bot.get_guild(int(ids[0]))
            # get the channel in the server
            linked_channel = linked_guild.get_channel(int(ids[1]))
            # get the message in the channel... in the server
            linked_message = await linked_channel.fetch_message(int(ids[2]))

            # get the possible urls
            urls = self.getMessageAttachmentURLs(linked_message)

            if len(urls) == 0:
                await ctx.send(":warning: Linked message does not have attached pictures.")
                return

        else: # result == None
            await ctx.send(":grey_question: You have not provided anything to perform reverse search on. If you want to learn how to use SauceBot, send `sauce.help`.")
            return

        index = 1
        # iterate over attachments and provide search links for them
        for u in urls:
            embed = discord.Embed(color=self.bot.embed_colors[ctx.guild.id])
            embed.set_thumbnail(url=self.bot.user.avatar_url)

            if result == "file":
                embed.title = ":mag_right: Reverse searching attached files"
                embed.add_field(name="Attachment {} of {}:".format(index, len(urls)), value=u, inline=False)

            elif result == "link":
                embed.title = ":mag_right: Reverse searching provided link"
                embed.add_field(name="Provided link:", value=u, inline=False)

            if result == "discord link":
                embed.title = ":mag_right: Reverse searching images attached to linked message"
                link = ctx.message.content.replace(ctx.prefix + ctx.invoked_with, "").strip()
                embed.add_field(name="Linked message:", value=link, inline=False)
                embed.add_field(name="Found attachment {} of {}:".format(index, len(urls)), value=u, inline=False)

            if saucenao == True:
                embed.add_field(name="\u200b", value="**[SauceNAO]({})\n**".format(self.sauceLink(u)), inline=False)
            if google == True:
                embed.add_field(name="\u200b", value="**[Google]({})\n**".format(self.googleLink(u)), inline=False)
            if tineye == True:
                embed.add_field(name="\u200b", value="**[TinEye]({})\n**".format(self.tineyeLink(u)), inline=False)
            if iqdb == True:
                embed.add_field(name="\u200b", value="**[IQDB]({})\n**".format(self.iqdbLink(u)), inline=False)
            if yandex == True:
                embed.add_field(name="\u200b", value="**[Yandex]({})**".format(self.yandexLink(u)), inline=False)

            await ctx.send(embed=embed)
            del embed
            index += 1
        return

    def sauceLink(self, url: str):
        return "https://saucenao.com/search.php?url={}".format(parse.quote_plus(url))

    def googleLink(self, url: str):
        return "https://www.google.com/searchbyimage?&image_url={}".format(parse.quote_plus(url))

    def tineyeLink(self, url: str):
        return "https://www.tineye.com/search?url={}".format(parse.quote_plus(url))

    def iqdbLink(self, url: str):
        return "https://iqdb.org/?url={}".format(parse.quote_plus(url))

    def yandexLink(self, url: str):
        return "https://yandex.com/images/search?url={}&rpt=imageview".format(parse.quote_plus(url))

    # ananlyze the command called by the user
    def analyzeCommand(self, ctx: commands.Context):
        # NOTE: I know that using strings as return values is rather lazy, but it's not meant to be a *high performance* bot

        # if message body is empty (there is no text after the command)
        if (ctx.prefix + ctx.invoked_with) == ctx.message.content:
            # if there is a file (or files) attached
            if len(ctx.message.attachments) > 0:
                return "file"
            else:
                # no message, no attachments.
                return None
        else:
            # the command is followed by some text, detect if that's a valid discord message permalink
            if re.search(r"https://(ptb\.|canary\.){0,1}discord(app){0,1}\.com/channels/\d+/\d+/\d+", ctx.message.content, re.I) != None:
                return "discord link"
            # if not, assume that's just a link to a picture. it's user's responsibility to make sure it's valid
            else:
                return "link"

    def getMessageAttachmentURLs(self, message: discord.Message):
        urls = []

        # iterate over attached files and get their urls
        for a in message.attachments:
            urls.append(a.url)

        return urls

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="SauceBot", description="Serving the sauce since 2018.", url="https://github.com/PoldekPL/SauceBot", color=self.bot.embed_colors[ctx.guild.id])
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="\u200b", value="SauceBot has one purpose, to make finding ~~sauce~~ source for pictures easier. Provide a picture, select one (or all) search engines and you'll be one click away from finding the original.", inline=False)
        embed.add_field(name="Usage", value="To learn about how to use the SauceBot, send a message with `sauce.help`.", inline=False)
        embed.set_footer(text="-- SauceBot written by PoldekPL#0105. --")
        await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx):
        pver = sys.version_info
        
        status_embed = discord.Embed(title="Ready.", color=self.bot.embed_colors[ctx.guild.id])
        status_embed.set_thumbnail(url=self.bot.user.avatar_url)
        status_embed.add_field(name="discord.py version:", value="%s, running under Python %d.%d.%d" % (discord.__version__, pver[0], pver[1], pver[2]))
        status_embed.set_footer(text="To read about how to use the SauceBot, use sauce.help")

        await ctx.send(embed=status_embed)

    @commands.command(name="help", aliases=["h"])
    async def helpCommand(self, ctx):
        for part in self.bot.sauce_help:
            await ctx.send(part)

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['reload'])
    async def restart(self, ctx):
        # log the use of restart command
        print("[{}]: Received restart command.".format(getLogFormattedTime()))

        # signal that bot is rebooting
        await ctx.message.add_reaction('♻')

        # save the message ids
        file = open(self.bot.current_path + "/restart_msg_id", "w")
        file.write(str(ctx.guild.id) + ' ' + str(ctx.channel.id) + ' ' + str(ctx.message.id))
        file.close()

        #save batch data
        self.bot.cogs["SauceBatch"].savefiles()

        # properly shut down
        await self.bot.logout()

        # restart
        print("[{}]: Rebooting...".format(getLogFormattedTime()))
        os.execl(os.path.abspath(__file__), " ")

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["loadfiles"])
    async def reloadfiles(self, ctx):
        print("[{}]: Reloading input files.".format(getLogFormattedTime()))
        self.bot.loadfiles()
        await ctx.message.add_reaction('✅')

def setup(bot):
    bot.add_cog(Announce(bot))
