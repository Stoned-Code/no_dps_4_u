from bot_commands import role_picker
from sc_libs.discord.help import SCHelp

def _register_commands(client):
    help = SCHelp(client)
    SCHelp.set_thumbnail('https://clipartcraft.com/images/overwatch-logo-transparent-large-6.png')
    role_picker.register_commands(client)
