import discord
import traceback
from discord.ext import commands
from cogs.utils.views import DropdownView


class Admin(commands.Cog):
    """A collection of admin-only commands."""

    def __init__(self, bot):
        self.bot = bot

    class EmbedFlags(commands.FlagConverter, case_insensitive=True, prefix='--', delimiter=' '):
        channel: discord.TextChannel = None
        title: str = ""
        description: str = ""
        image: str = ""
        footer: str = ""
        colour: str = str(discord.Colour.og_blurple())[1:]

    class DropdownFlags(commands.FlagConverter, case_insensitive=True, prefix='--', delimiter=' '):
        name: str
        description: str
        emoji: str
        role: int

    @staticmethod
    def create_embed(flags: EmbedFlags):
        embed = discord.Embed()

        embed = embed.from_dict({'title': f'{flags.title}',
                                 'description': f'{flags.description}',
                                 'image': {'url': f'{flags.image}'},
                                 'footer': {'text': f'{flags.footer}'},
                                 'color': int(flags.colour, 16),
                                 })
        return embed

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx, *, flags: EmbedFlags):
        """
        A flag-based embed generator.

        --title
        --description
        --image
        --footer
        --colour: hex colour code
        """

        if flags.channel is None:
            flags.channel = ctx.channel

        try:
            embed = self.create_embed(flags)

        except discord.errors.HTTPException as error:
            if error.code == 50035:  # cannot send nothing
                traceback.print_exception(type(error), error, error.__traceback__)
                return await ctx.send("Embed cannot be empty. Aborted.")
            else:
                raise

        confirm = await ctx.prompt(
            f"The following embed will be sent to {flags.channel}. Are you sure?",
            embed=embed
        )
        if not confirm:
            return await ctx.send("Aborting.")

        await flags.channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def dropdown(self, ctx, channel: discord.TextChannel, role_num: int, min_roles: int, max_roles: int, *,
                       placeholder):
        """
        An interactive dropdown creator.

        --name: label of the role to be displayed.
        --description: description of the role.
        --emoji: emoji of the role.
        --role: the role's ID.
        """

        max_id = (await(await self.bot.db.execute("""SELECT MAX(dropdown_num) FROM dropdowns""")).fetchone())[0]
        if max_id is None:
            max_id = 0

        def check(message):
            return ctx.author.id == message.author.id and ctx.channel.id == message.channel.id

        roles = []

        await ctx.send(f"Hello. Please enter the desired role for your dropdown **{role_num}** times.")

        for i in range(role_num):
            msg = await ctx.bot.wait_for("message", check=check, timeout=600.0)

            flags = await Admin.DropdownFlags.convert(ctx, msg.content)

            roles.append([flags.name, flags.description, flags.emoji, flags.role])

            await self.bot.db.execute("""INSERT INTO dropdowns (name, description, emoji, id, dropdown_num)
                                        VALUES (?, ?, ?, ?, ?)""",
                                      (flags.name, flags.description, flags.emoji, flags.role, max_id + 1))

        await self.bot.db.commit()

        view = DropdownView(roles, placeholder, min_roles, max_roles)

        await ctx.send("Please enter the embed to be attached to the dropdown.")

        msg = await ctx.bot.wait_for("message", check=check, timeout=600.0)
        flags = await self.EmbedFlags.convert(ctx, msg.content)
        embed = self.create_embed(flags)

        confirm = await ctx.prompt(
            f"The following dropdown will be sent to {channel}. Are you sure?",
            embed=embed
        )

        if not confirm:
            return await ctx.send("Aborting.")

        msg = await channel.send(embed=embed, view=view)

        await self.bot.db.execute("""UPDATE dropdowns SET message_id = ? WHERE dropdown_num = ? """, (msg.id, max_id + 1))
        await self.bot.db.commit()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, channel: discord.TextChannel, *, content):
        await channel.send(content)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def sql(self, ctx, *, query: str):
        """Executes some sql. (fetch)"""

        rows = await self.bot.db.execute(query)
        rows = await rows.fetchall()

        await ctx.send(rows)

        # rows = await self.bot.db.execute("""SELECT * FROM users WHERE user_id = ?""", (ctx.member.id,))
        # rows = await rows.fetchall()

    @sql.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def run(self, ctx, *, query: str):
        """Executes some sql. (runs stuff)"""

        await self.bot.db.execute(query)

        confirm = await ctx.prompt(
            f"Do you want to execute this query? \n"
            f"```{query}```",
        )
        if not confirm:
            return await ctx.send("Aborting.")

        await self.bot.db.commit()


async def setup(bot):
    await bot.add_cog(Admin(bot))
