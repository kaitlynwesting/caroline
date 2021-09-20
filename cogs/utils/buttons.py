import asyncio
import discord
from discord.ext import commands


class PaginationView(discord.ui.View):
    def __init__(
        self,
        embed_list,
        *,
        ctx: commands.Context,
    ):

        super().__init__(timeout=60.0)
        self.ctx: commands.Context = ctx
        self.current = 0
        self.embed_list = embed_list

        if len(embed_list) == 1:
            self.clear_items()

    # What occurs on timeout
    async def on_timeout(self) -> None:
        self.clear_items()
        await self.message.edit(view=self)

    # Checks if the invoking author is pressing the buttons
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.user == interaction.user:
            return True
        await interaction.response.send_message(
            f"Only {self.user.name} can react. Start a new instance if you want"
            f"to be able to browse.",
            ephemeral=True,
        )
        return False

    def update_buttons(self, button: discord.ui.Button) -> None:

        if button == self.previous:
            self.current -= 1
            self.next.disabled = False
            self.last.disabled = False
        elif button == self.next:
            self.current += 1
            self.previous.disabled = False
            self.first.disabled = False
        elif button == self.first:
            self.current = 0
            self.previous.disabled = True
            self.first.disabled = True
            self.next.disabled = False
            self.last.disabled = False
            return
        elif button == self.last:
            self.current = len(self.embed_list) - 1
            self.next.disabled = True
            self.last.disabled = True
            self.previous.disabled = False
            self.first.disabled = False
            return
        if self.current == 0:
            self.previous.disabled = True
            self.first.disabled = True
            self.next.disabled = False
            self.last.disabled = False
        elif self.current == len(self.embed_list) - 1:
            self.previous.disabled = False
            self.first.disabled = False
            self.next.disabled = True
            self.last.disabled = True

    @discord.ui.button(label="<<", style=discord.ButtonStyle.secondary, disabled=True)
    async def first(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.update_buttons(button)
        await interaction.response.edit_message(
            embed=self.embed_list[self.current], view=self
        )

    @discord.ui.button(label="Back", style=discord.ButtonStyle.blurple, disabled=True)
    async def previous(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.update_buttons(button)
        await interaction.response.edit_message(
            embed=self.embed_list[self.current], view=self
        )

    @discord.ui.button(label="Skip to", style=discord.ButtonStyle.primary)
    async def skipto(self, button: discord.ui.Button, interaction: discord.Interaction):

        channel = self.message.channel
        author_id = interaction.user and interaction.user.id
        await interaction.response.send_message(
            f"What page do you want to go to?", ephemeral=True
        )

        def check(message):
            return (
                author_id == message.author.id
                and channel.id == message.channel.id
                and message.content.isdigit()
            )

        try:
            msg = await self.ctx.bot.wait_for("message", check=check, timeout=30.0)
            self.current = int(msg.content) - 1
            self.update_buttons(button)
            await interaction.message.edit(
                embed=self.embed_list[self.current], view=self
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("Took too long. Goodbye.", ephemeral=True)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.update_buttons(button)
        await interaction.response.edit_message(
            embed=self.embed_list[self.current], view=self
        )

    @discord.ui.button(label=">>", style=discord.ButtonStyle.secondary)
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.update_buttons(button)
        await interaction.response.edit_message(
            embed=self.embed_list[self.current], view=self
        )

    @discord.ui.button(label="Quit", style=discord.ButtonStyle.red)
    async def quit(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.clear_items()
        await interaction.response.edit_message(
            embed=self.embed_list[self.current], view=self
        )

    # Starting the pagination view
    async def start(self, ctx, notification_context):
        self.message = await notification_context.send(
            embed=self.embed_list[0], view=self
        )
        self.user = ctx.author
        return self.message
