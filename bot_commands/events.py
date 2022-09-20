import abc
from subprocess import call

import config
import discord
from discord.ext.commands import Bot

reaction_callbacks = []

def add_reaction_callback(callback):
    reaction_callbacks.append(callback)

    
def register_events(client: Bot):
    @client.event
    async def on_ready(): 
        """
        Prints bot info on ready.
        """
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='{}help'.format(config.PREFIX)))
        print('Bot logged in as {}.'.format(client.user))
        print('Prefix: {}'.format(config.PREFIX))
    
    @client.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        for callback in reaction_callbacks:
            try:
                await callback(payload)
            
            except Exception as ex:
                print('Something Broke:\n{}'.format(ex.with_traceback()))


        