# Invite Link: https://discord.com/api/oauth2/authorize?client_id=1018666425566646332&permissions=274877982784&scope=bot
# Build Command: pyinstaller --onefile --noupx main.py -n "No DPS"

import config
import discord
from discord.ext import commands
from sc_libs.discord.command import Command
import bot_commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix = config.PREFIX, intents = intents)
Command.set_prefix(config.PREFIX)

@client.event
async def on_ready():
    print('Bot logged in as {}.'.format(client.user))

bot_commands._register_commands(client)
client.run(config.TOKEN)