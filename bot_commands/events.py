import discord
import config
from discord.ext.commands import Bot

def register_events(client: Bot):
    @client.event
    async def on_ready(): 
        """
        Prints bot info on ready.
        """
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='{}help'.format(config.PREFIX)))
        print('Bot logged in as {}.'.format(client.user))
        print('Prefix: {}'.format(config.PREFIX))