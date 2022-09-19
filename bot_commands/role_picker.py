
from macpath import split
from bot_commands.enums.Roles import ReRollTypes
from bot_commands.events import add_reaction_callback
import config
import discord
from discord import Emoji, Embed
from discord.ext.commands.context import Context
from sc_libs.discord.command import SCCommand
from sc_libs.discord.command_class import Command_Class
from sc_libs.utils.conversions import tuple_to_list, list_to_tuple
from sc_libs.utils.random import choices

max_player_count = 6

class RolePicker(Command_Class):
    previous_damage = ()
    previous_tanks = ()
    previous_healers = ()
    previous_team = ()
    def __init__(self, client):
        super().__init__(client)
        add_reaction_callback(self.on_reaction)

    async def on_reaction(self, payload):
        if payload.channel_id not in config.BOT_CHANNEL_IDS or payload.user_id == self.bot_client.user.id:
            return
            
        msg_id = payload.message_id
        channel_id = payload.channel_id
        channel: discord.TextChannel = self.bot_client.get_channel(channel_id)

        split_reroll = config.REROLL_REACTION.split(':')

        if payload.emoji.id == None:
            if len(split_reroll) == 1:
                emoji_flag = payload.emoji.name == config.REROLL_REACTION

            elif len(split_reroll) == 3:
                names_match = payload.emoji.name.lower() == config.REROLL_REACTION.split(':')[1].lower()
                ids_match = payload.emoji.id == int(config.REROLL_REACTION.split(':')[2])
                emoji_flag =  names_match and ids_match
        else:
            if len(split_reroll) == 1:
                emoji_flag = False
            else:
                names_match = payload.emoji.name.lower() == config.REROLL_REACTION.split(':')[1].lower()
                ids_match = payload.emoji.id == int(config.REROLL_REACTION.split(':')[2])
                emoji_flag =  names_match and ids_match

        if not emoji_flag:
            return

        reroll_info = self.get_reroll_message(msg_id)
        success = reroll_info[0]
        role = reroll_info[1]

        if not success:
            return

        if role == ReRollTypes.DAMAGE:

            await self.reroll_damage(channel)

        elif role == ReRollTypes.HEALER:
            await self.reroll_healers(channel)
        
        elif role == ReRollTypes.TANK:
            await self.reroll_tank(channel)

        elif role == ReRollTypes.TEAM:
            await self.reroll_team(channel)

    def get_reroll_message(self, id):
        dmg_available = len(self.previous_damage) != 0
        healer_available = len(self.previous_healers) != 0
        tank_available =  len(self.previous_tanks) != 0
        team_available = len(self.previous_team) != 0

        is_reroll_msg = team_available and self.previous_team[0] == id or dmg_available and self.previous_damage[0] == id or healer_available and self.previous_healers[0] == id or tank_available and self.previous_tanks[0] == id

        if not is_reroll_msg:
            return False


        reroll_info = [self.previous_damage, self.previous_healers, self.previous_tanks, self.previous_team]
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

            if ctx.channel.id not in config.BOT_CHANNEL_IDS:
                await ctx.send('Can\'t post in this channel.')
                return

            args = tuple_to_list(args)
            tanks = choices(args, 2)
            msg: discord.Message = await ctx.send('Your chosen tanks are: {}'.format(', '.join(tanks)))

            self.set_previous_tanks(msg.id, tuple_to_list(args))

            await self.add_reaction(msg)


        @SCCommand(name = 'heals', category = 'Role Picker', description = 'Picks healers from given names.', example = 'heal {name 1} {name 2} {name...}')
        @self.bot_client.command()
        async def heals(ctx: Context, *args):
            if args == None or len(args) == 0:
                await ctx.send('Where the healers at?')
                return

            if ctx.channel.id not in config.BOT_CHANNEL_IDS:
                await ctx.send('Can\'t post in this channel.')
                return

            args = tuple_to_list(args)
            healers = choices(args, 2)
            msg: discord.Message = await ctx.send('Your chosen healers are: {}'.format(', '.join(healers)))

            self.set_previous_healers(msg.id, tuple_to_list(args))

            await self.add_reaction(msg)
        
        @SCCommand(name = 'team', category = 'Role Picker', description = 'Give {} player names and it\'ll spit out their roles.'.format(max_player_count), example = 'team {name 1} {name 2} {name...} {name 6')
        @self.bot_client.command()
        async def team(ctx: Context, *args):
            if len(args) < max_player_count:
                ex = 'You need {} amount of names, you only gave {}.'(max_player_count, len(args))
                await ctx.send(ex)
                return

            if ctx.channel.id not in config.BOT_CHANNEL_IDS:
                await ctx.send('Can\'t post in this channel.')
                return

            player_list = tuple_to_list(args)

            dps = choices(player_list, 2)
            player_list = [player for player in player_list if player not in dps]
            tanks = choices(player_list, 2) # Change in OW2.
            healers = [player for player in player_list if player not in tanks]

            print(dps)
            print(tanks)
            print(healers)

            embed = Embed(title = 'Team Roles', description = 'You\'re role composition is as follows.')
            embed.set_thumbnail(url = 'https://clipartcraft.com/images/overwatch-logo-transparent-large-6.png')
            embed.set_image(url = 'https://www.slashgear.com/wp-content/uploads/2020/01/Overwatch-2.jpg')

            embed.add_field(name = 'Tanks', value = '\n'.join(tanks))
            embed.add_field(name = 'Damage', value = '\n'.join(dps))
            embed.add_field(name = 'Healers', value = '\n'.join(healers))

            msg: discord.Message = await ctx.send(embed = embed)

            self.set_previous_team(msg.id, tuple_to_list(args))

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
        self.previous_damage = list_to_tuple([msg_id, ReRollTypes.DAMAGE, dps])
    
    def set_previous_tanks(self, msg_id, tanks):
        self.previous_tanks = list_to_tuple([msg_id, ReRollTypes.TANK, tanks])

    def set_previous_healers(self, msg_id, healers):
        self.previous_healers = list_to_tuple([msg_id, ReRollTypes.HEALER, healers])

    def set_previous_team(self, msg_id, team):
        self.previous_team = list_to_tuple([msg_id, ReRollTypes.TEAM, team])

    async def reroll_team(self, channel: discord.TextChannel):
        player_list = list(self.previous_team[2])

        if len(player_list) == 0:
            await channel.send('Team command has yet to be used. Do `{0}help team`'.format(config.PREFIX))
            return

        dps = choices(player_list, 2)
        player_list = [player for player in player_list if player not in dps]
        tanks = choices(player_list, 2) # Change in OW2.
        healers = [player for player in player_list if player not in tanks]

        embed = Embed(title = 'Team Roles', description = 'You\'re role composition is as follows.')
        embed.set_thumbnail(url = 'https://clipartcraft.com/images/overwatch-logo-transparent-large-6.png')
        embed.set_image(url = 'https://www.slashgear.com/wp-content/uploads/2020/01/Overwatch-2.jpg')

        embed.add_field(name = 'Tanks', value = '\n'.join(tanks))
        embed.add_field(name = 'Damage', value = '\n'.join(dps))
        embed.add_field(name = 'Healers', value = '\n'.join(healers))

        msg: discord.Message = await channel.send(embed = embed)

        self.set_previous_team(msg.id, self.previous_team[2])

        await self.add_reaction(msg)       


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

        tanks = choices(args, 2)
        msg = await channel.send('Your chosen tanks are: {}'.format(', '.join(tanks)))
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

