from discord.ext import commands
from sc_libs.discord.help import SCHelp

from bot_commands.owner import Owner
from bot_commands.role_picker import RolePicker
from bot_commands import events

maximum_player_count = 6

def register_bot_commands(client: commands.Bot) -> None:
    """
    Registers the bot's commands.

    Arguments:
    ----------
    client: `discord.ext.commands.context.Context`
        The discord bot client.
    """
    
    events.register_events(client) # Registers the bot events.

    sc_help = SCHelp(client) # Registers the SCHelp command instead of the default discord.py help command.
    role_picker = RolePicker(client) # Registers role picker commands.
    owner = Owner(client) # Registers owner commands.
    
    SCHelp.set_bot_description('A bot for Overwatch gaming stuffs, I don\'t know I\'m high.') # Sets the bot's description.
    SCHelp.set_thumbnail('https://clipartcraft.com/images/overwatch-logo-transparent-large-6.png') # Sets the thumbnail for the help command.

