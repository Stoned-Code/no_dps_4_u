from macpath import split
from bot_commands.enums.Roles import Role
import config
import discord
from discord import Emoji
from discord.ext.commands.context import Context
from sc_libs.discord.command import SCCommand
from sc_libs.discord.command_class import Command_Class
from sc_libs.utils.conversions import tuple_to_list, list_to_tuple
from sc_libs.utils.random import choices


class RolePicker(Command_Class):
    previous_damage = ()
    previous_tanks = ()
    previous_healers = ()

    def get_reroll_message(self, id):
        is_reroll_msg = self.previous_damage[0] == id or self.previous_healers[0] == id or self.previous_tanks[0] == id

        if not is_reroll_msg:
            return False


        reroll_info = [self.previous_damage, self.previous_healers, self.previous_tanks]
        reroll_info = [item for item in reroll_info if len(item) == 3 and item[0] == id]
        reroll_info = reroll_info[0]
        if len(reroll_info) != 3:
            return False

        return tuple([True, reroll_info[1]])

    @property
    def damage_available(self):
        return len(self.previous_damage) == 3

    @property
    def tanks_available(self):
        return len(self.previous_tanks) == 3

    @property
    def healers_available(self):
        return len(self.previous_healers) == 3

    def load_commands(self) -> None:

        @SCCommand(name = 'damage', category = 'Role Picker', description = 'Picks dps from given names.', example = 'damage {name 1} {name 2} {name...}')
        @self.bot_client.command()
        async def damage(ctx: Context, *args):
            if args == None or len(args) == 0:
                await ctx.send('Where the DPS at?')
                return

            if ctx.channel.id not in config.BOT_CHANNEL_IDS:
                await ctx.send('Can\'t post in this channel.')
                return

            args = tuple_to_list(args)
            dps = choices(args, 2)
            msg: discord.Message = await ctx.send('Your chosen DPS are: {}'.format(', '.join(dps)))

            self.set_previous_damage(msg.id, tuple_to_list(args))

            await self.add_reaction(msg)


        @SCCommand(name = 'tank', category = 'Role Picker', description = 'Picks tanks from given names.', example = 'tank {name 1} {name 2} {name...}')
        @self.bot_client.command()
        async def tank(ctx: Context, *args):
            if args == None or len(args) == 0:
                await ctx.send('Where the tanks at?')
                return

            if ctx.channel.id not in config.BOT_CHANNEL_ID:
                await ctx.send('Can\'t post in this channel.')
                return

            args = tuple_to_list(args)
            tanks = choices(args, 1)
            msg: discord.Message = await ctx.send('Your chosen tank is: {}'.format(', '.join(tanks)))

            self.set_previous_tanks(msg.id, tuple_to_list(args))

            await self.add_reaction(msg)


        @SCCommand(name = 'heals', category = 'Role Picker', description = 'Picks healers from given names.', example = 'heal {name 1} {name 2} {name...}')
        @self.bot_client.command()
        async def heals(ctx: Context, *args):
            if args == None or len(args) == 0:
                await ctx.send('Where the healers at?')
                return

            if ctx.channel.id not in config.BOT_CHANNEL_ID:
                await ctx.send('Can\'t post in this channel.')
                return

            args = tuple_to_list(args)
            healers = choices(args, 2)
            msg: discord.Message = await ctx.send('Your chosen healers are: {}'.format(', '.join(healers)))

            self.set_previous_healers(msg.id, tuple_to_list(args))

            await self.add_reaction(msg)


    async def add_reaction(self, msg):
        split_reaction = config.REROLL_REACTION.split(':')

        if len(split_reaction) == 3:
            emojis = self._client.emojis
            emojis = [emoji for emoji in emojis if emoji.name == split_reaction[1] and emoji.id == int(split_reaction[2])]

            if len(emojis) > 0:
                emoji = emojis[0]
            else:
                emoji = None
        else:
            emoji = config.REROLL_REACTION

        if emoji != None:
            await msg.add_reaction(emoji)

    def set_previous_damage(self, msg_id, dps):
        self.previous_damage = list_to_tuple([msg_id, Role.DAMAGE, dps])
    
    def set_previous_tanks(self, msg_id, tanks):
        self.previous_tanks = list_to_tuple([msg_id, Role.TANK, tanks])

    def set_previous_healers(self, msg_id, healers):
        self.previous_healers = list_to_tuple([msg_id, Role.HEALER, healers])



    async def reroll_damage(self, channel: discord.TextChannel):
        args = self.previous_damage[2]
        if len(args) == 0:
            await channel.send('Damage command has yet to be used. Do `{0}help damage`'.format(config.PREFIX))
            return

        dps = choices(args, 2)

        msg = await channel.send('Your chosen DPS are: {}'.format(', '.join(dps)))
        self.set_previous_damage(msg.id, args)
        await self.add_reaction(msg)

    async def reroll_tank(self, channel: discord.TextChannel):
        args = self.previous_tanks[2]
        if len(args) == 0:
            await channel.send('Tank command has yet to be used. Do `{0}help tank`'.format(config.PREFIX))
            return

        tanks = choices(args)
        msg = await channel.send('Your chosen tank is: {}'.format(tanks[0]))
        self.set_previous_tanks(msg.id, args)
        await self.add_reaction(msg)
        
    async def reroll_healers(self, channel: discord.TextChannel):
        args = self.previous_healers[2]
        if len(args) == 0:
            await channel.send('Heals command has yet to be used. Do `{0}help heals`'.format(config.PREFIX))
            return
        
        heals = choices(args, 2)
        msg = await channel.send('Your chosen healers are: {}'.format(', '.join(heals)))

        self.set_previous_healers(msg.id, args)
        await self.add_reaction(msg)

