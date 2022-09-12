# Build Command: pyinstaller --onefile --noupx main.py -n "OverwatchSC Bot"

import config # Imports the config. (Create a "config.py" file with the TOKEN, PREFIX and PORT in it.)
import discord # Import discord.py library.
from discord.ext import commands # Imports the commands script.
from sc_libs.discord.command import Command # Imports the sc_libs Command class.
import bot_commands # Imports the bot commands.

intents = discord.Intents.default() # Creates a default intent object.
intents.members = True # Enables member intents.
intents.guilds = True # Enables guild intents.

client = commands.Bot(command_prefix = config.PREFIX, intents = intents) # Creates discord bot client.
Command.set_prefix(config.PREFIX) # Sets the prefix for the help command info.

@client.event
async def on_ready(): 
    """
    Prints bot info on ready.
    """
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='{}help'.format(config.PREFIX)))
    print('Bot logged in as {}.'.format(client.user))
    print('Prefix: {}'.format(config.PREFIX))
    print('Port: {}'.format(config.PORT))

bot_commands.register_bot_commands(client) # Registers the bot commands.
client.run(config.TOKEN) # Runs the discord bot.