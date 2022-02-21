import discord
from discord.ext import commands
from cogs.utils import constants


# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Announcements', description='Major server announcements', emoji='📢'),
            discord.SelectOption(label='Seasonal Events',
                                 description='New events with periodic prizes',
                                 emoji='🎟️'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose your notification roles.', min_values=0, max_values=2, options=options,
                         custom_id='persistent_view:dropdown')
        self.persistent_views_added = False

    async def callback(self, interaction: discord.Interaction):
        role_mapping = {'Announcements': constants.announcements_role,
                        'Seasonal Events': constants.weekly_events_role}

        def without_keys(d, keys):
            return {x: d[x] for x in d if x not in keys}

        # This indicates that options were removed by the user.
        if not self.values:
            for role in role_mapping:
                role = interaction.guild.get_role(role_mapping[role])
                await interaction.user.remove_roles(role)

            await interaction.response.send_message(f'All selectable roles were removed.', ephemeral=True)
            return

        # If at least one value remains selected
        for value in self.values:
            role = interaction.guild.get_role(role_mapping[value])
            await interaction.user.add_roles(role)

        for key in without_keys(role_mapping, set(self.values)):
            role = interaction.guild.get_role(role_mapping[key])
            await interaction.user.remove_roles(role)

        await interaction.response.send_message(f"Success. You are currently subscribed to the following: "
                                                f"**{', '.join(self.values)}**", ephemeral=True)


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


class Dropdowns(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def colour(self, ctx):
        """Sends a message with our dropdown containing colours"""

        # Create the view containing our dropdown
        view = DropdownView()

        # Sending a message containing our view
        embed = discord.Embed.from_dict({'title': f'Notification Roles',
                                         'description': f'Subscribe to these roles to get notified for their respective '
                                                        f'categories. '
                                                        f'Note that some events may require that you have the '
                                                        f'<@&860240614041452544> role to participate.',
                                         'footer': {'text': f'If the interactions fails, wait to retry. If the issue '
                                                            f'persists, open a ticket.'},
                                         'color': constants.blurple,
                                         })
        await ctx.send(view=view, embed=embed)


def setup(bot):
    bot.add_cog(Dropdowns(bot))
