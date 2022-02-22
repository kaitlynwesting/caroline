import asyncio
import discord
from discord.ext import commands
from typing import Optional


class Context(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def prompt(
            self,
            message: str,
            *,
            timeout: float = 60.0,
            delete_after: bool = True,
            author_id: Optional[int] = None,
    ) -> Optional[bool]:
        """An interactive reaction confirmation dialog.
        Parameters
        -----------
        message: str
            The message to show along with the prompt.
        timeout: float
            How long to wait before returning.
        delete_after: bool
            Whether to delete the confirmation message after we're done.
        author_id: Optional[int]
            The member who should respond to the prompt. Defaults to the author of the
            Context's message.
        Returns
        --------
        Optional[bool]
            ``True`` if explicit confirm,
            ``False`` if explicit deny,
            ``None`` if deny due to timeout
        """

        author_id = author_id or self.author.id
        view = ConfirmationView(
            timeout=timeout,
            delete_after=delete_after,
            ctx=self,
            author_id=author_id,
        )
        view.message = await self.send(message, view=view)
        await view.wait()
        return view.value


class ConfirmationView(discord.ui.View):
    def __init__(self, *, timeout: float, author_id: int, ctx: Context, delete_after: bool) -> None:
        super().__init__(timeout=timeout)
        self.value: Optional[bool] = None
        self.delete_after: bool = delete_after
        self.author_id: int = author_id
        self.ctx: Context = ctx
        self.message: Optional[discord.Message] = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.user.id == self.author_id:
            return True
        else:
            await interaction.response.send_message('This confirmation dialogue is not for you.', ephemeral=True)
            return False

    async def on_timeout(self) -> None:
        if self.delete_after:
            await self.message.delete()

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        await interaction.response.defer()
        if self.delete_after:
            await interaction.delete_original_message()
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        await interaction.response.defer()
        if self.delete_after:
            await interaction.delete_original_message()
        self.stop()


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
            f"Only {self.user.name} can react. Start a new instance if you want browse.",
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
