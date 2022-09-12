import discord
from discord.ext import commands
from sc_libs.discord.command import SCCommand
from sc_libs.discord.command_class import Command_Class


class Owner(Command_Class):
    def load_commands(self):
        @SCCommand(name = 'debug', category = 'Owner', description = 'Owner command.')
        @commands.is_owner()
        @self.bot_client.command()
        async def debug(ctx: discord.ext.commands.context.Context):
            pass
