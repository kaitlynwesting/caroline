import discord
import traceback
from discord.ext import commands


class Admin(commands.Cog):
    """A collection of admin-only commands."""

    def __init__(self, bot):
        self.bot = bot

    class EmbedFlags(commands.FlagConverter, prefix='--', delimiter=' '):
        channel: discord.TextChannel = None
        title: str = ""
        description: str = ""
        image: str = ""
        footer: str = ""
        colour: str = str(discord.Colour.og_blurple())

    @commands.command(hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def embed(self, ctx, *, flags: EmbedFlags):
        """
        A utility to create embeds via command.
        """

        if flags.channel is None:
            flags.channel = ctx.channel

        embed = discord.Embed()

        try:
            embed = embed.from_dict({'title': f'{flags.title}',
                                     'description': f'{flags.description}',
                                     'image': {'url': f'{flags.image}'},
                                     'footer': {'text': f'{flags.footer}'},
                                     'color': int(flags.colour, 16),
                                     })
        except discord.errors.HTTPException as error:
            if error.code == 50035:  # cannot send nothing
                traceback.print_exception(type(error), error, error.__traceback__)
                return await ctx.send("Embed cannot be empty. Aborted.")
            else:
                raise

        confirm = await ctx.prompt(
            f"The following embed will be sent to {flags.channel}. Are you sure?**",
            embed=embed
        )
        if not confirm:
            return await ctx.send("Aborting.")

        await flags.channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, channel: discord.TextChannel, *, content: str):
        await channel.send(content)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def sql(self, ctx, *, query: str):
        """Executes some sql. (fetch)"""

        rows = await self.bot.db.execute(query)
        rows = await rows.fetchall()

        await ctx.send(rows)

        # rows = await self.bot.db.execute("""SELECT * FROM users WHERE user_id = ?""", (ctx.member.id,))
        # rows = await rows.fetchall()


async def setup(bot):
    await bot.add_cog(Admin(bot))
