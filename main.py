import os

import discord  # Import discord.py library.
from discord.ext import commands  # Imports the commands script.

import config  # Imports the config. (Create a "config.py" file with the TOKEN, PREFIX and PORT in it.)
from bot_commands import register_bot_commands  # Imports the bot commands.
from sc_libs.discord.command import \
    SCCommand  # Imports the sc_libs Command class.

client = commands.Bot(command_prefix = config.PREFIX) # Creates discord bot client.
SCCommand.set_prefix(config.PREFIX) # Sets the prefix for the help command info.
register_bot_commands(client) # Registers the bot commands.
client.run(config.TOKEN) # Runs the discord bot.
