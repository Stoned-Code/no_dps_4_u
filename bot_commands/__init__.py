from bot_commands.role_picker import RolePicker
from sc_libs.discord.help import SCHelp
from discord.ext import commands

def register_bot_commands(client: commands.Bot) -> None:
    """
    Registers the bot's commands.

    Arguments:
    ----------
    client: `commands.Bot`
        The discord bot client.
    """

    help = SCHelp(client) # Registers the SCHelp command instead of the default discord.py help command.
    SCHelp.bot_description = 'A bot for Overwatch gaming stuffs, I don\'t know I\'m high.'
    SCHelp.set_thumbnail('https://clipartcraft.com/images/overwatch-logo-transparent-large-6.png') # Sets the thumbnail for the help command.
    role_picker = RolePicker(client)
