import discord
from discord.ext import commands
from sc_libs.discord.command import Command
from utils.random import choices
from utils.conversions import tuple_to_list
maximum_player_count = 6

def register_commands(client):

    @Command(name = 'damage', category = 'Role Picker', description = 'Picks dps from given names.', example = 'damage {name 1} {name 2} {name...}')
    @client.command()
    async def damage(ctx, *args):
        # if len(args) > maximum_player_count:
        #     ctx.send('To many people. Sad game.')
        #     return
        if args == None or len(args) == 0:
            await ctx.send('Where the DPS at?')
            return
        args = tuple_to_list(args)
        dps = choices(args, 2)
        await ctx.send('Your chosen DPS are: {}'.format(', '.join(dps)))


    @Command(name = 'tanks', category = 'Role Picker', description = 'Picks tanks from given names.', example = 'tank {name 1} {name 2} {name...}')
    @client.command()
    async def tanks(ctx, *args):
        # if len(args) > maximum_player_count:
        #     ctx.send('To many people. Sad game.')
        #     return
        if args == None or len(args) == 0:
            await ctx.send('Where the tanks at?')
            return

        args = tuple_to_list(args)
        tanks = choices(args, 1)
        await ctx.send('Your chosen tanks are: {}'.format(', '.join(tanks)))


    @Command(name = 'heals', category = 'Role Picker', description = 'Picks healers from given names.', example = 'heal {name 1} {name 2} {name...}')
    @client.command()
    async def heals(ctx, *args):
        # if len(args) > maximum_player_count:
        #     ctx.send('To many people. Sad game.')
        #     return
        if args == None or len(args) == 0:
            await ctx.send('Where the healers at?')
            return
        args = tuple_to_list(args)
        healers = choices(args, 2)
        await ctx.send('Your chosen healers are: {}'.format(', '.join(healers)))

