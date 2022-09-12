import config
import discord
from discord.ext.commands.context import Context
from sc_libs.discord.command import SCCommand
from sc_libs.discord.command_class import Command_Class
from sc_libs.utils.conversions import tuple_to_list
from sc_libs.utils.random import choices


class RolePicker(Command_Class):
    previous_damage = []
    previous_tanks = []
    previous_healers = []

    def load_commands(self) -> None:

        @SCCommand(name = 'damage', category = 'Role Picker', description = 'Picks dps from given names.', example = 'damage {name 1} {name 2} {name...}')
        @self.bot_client.command()
        async def damage(ctx: Context, *args):
            self.previous_damage = tuple_to_list(args)

            if args == None or len(args) == 0:
                await ctx.send('Where the DPS at?')
                return
            args = tuple_to_list(args)
            dps = choices(args, 2)
            await ctx.send('Your chosen DPS are: {}'.format(', '.join(dps)))
    

        @SCCommand(name = 'reroll_damage', category = 'Role Picker', description = 'Re-rolls the previous inputed names for two more damage players.')
        @self.bot_client.command()
        async def reroll_damage(ctx: discord.ext.commands.context.Context):
            if len(self.previous_damage) == 0:
                await ctx.send('Damage command has yet to be used. Do `{0}help damage`'.format(config.PREFIX))
                return

            args = list(self.previous_damage)
            dps = choices(args, 2)
            await ctx.send('Your chosen DPS are: {}'.format(', '.join(dps)))
        

        @SCCommand(name = 'tank', category = 'Role Picker', description = 'Picks tanks from given names.', example = 'tank {name 1} {name 2} {name...}')
        @self.bot_client.command()
        async def tank(ctx: discord.ext.commands.context.Context, *args):

            self.previous_tanks = tuple_to_list(args)

            if args == None or len(args) == 0:
                await ctx.send('Where the tanks at?')
                return

            args = tuple_to_list(args)
            tanks = choices(args, 1)
            await ctx.send('Your chosen tank is: {}'.format(', '.join(tanks)))


        @SCCommand(name = 'reroll_tank', category = 'Role Picker', description = 'Re-rolls the previous inputed tank names for another tank player.')
        @self.bot_client.command() 
        async def reroll_tank(ctx: discord.ext.commands.context.Context):
            if len(self.previous_tanks) == 0:
                await ctx.send('Tank command has yet to be used. Do `{0}help tank`'.format(config.PREFIX))
                return

            args = list(self.previous_tanks)
            tanks = choices(args)
            await ctx.send('Your chosen tank is: {}'.format(tanks[0]))


        @SCCommand(name = 'heals', category = 'Role Picker', description = 'Picks healers from given names.', example = 'heal {name 1} {name 2} {name...}')
        @self.bot_client.command()
        async def heals(ctx: discord.ext.commands.context.Context, *args):

            self.previous_healers = tuple_to_list(args)

            if args == None or len(args) == 0:
                await ctx.send('Where the healers at?')
                return
            args = tuple_to_list(args)
            healers = choices(args, 2)
            await ctx.send('Your chosen healers are: {}'.format(', '.join(healers)))


        @SCCommand(name = 'reroll_healers', category = 'Role Picker', description = 'Re-rolls the previous inputed names for two more healers.')
        @self.bot_client.command()
        async def reroll_healers(ctx: discord.ext.commands.context.Context):
            if len(self.previous_healers) == 0:
                await ctx.send('Heals command has yet to be used. Do `{0}help heals`'.format(config.PREFIX))
                return
            
            args = list(self.previous_healers)
            heals = choices(args, 2)
            await ctx.send('Your chosen healers are: {}'.format(', '.join(heals)))
