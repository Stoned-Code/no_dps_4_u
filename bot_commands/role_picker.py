import config
import discord
from discord import Embed, Emoji
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from enums.roles import ReRollTypes
from sc_libs.discord.command import SCCommand
from sc_libs.discord.command_class import Command_Class
from sc_libs.utils.conversions import list_to_tuple, tuple_to_list
from sc_libs.utils.random import choices

from bot_commands.events import add_reaction_callback

max_player_count = 6

class RolePicker(Command_Class):
    previous_damage = () # Previous information on the damage command.
    previous_tanks = () # Previous information on the tank command.
    previous_healers = () # Previous information on the healing command. 
    previous_team = () # Previous information on the team command.

    def __init__(self, client: Bot):
        super().__init__(client) # Initialized the base class.
        add_reaction_callback(self.on_reaction) # Adds a callback to the "on_raw_reaction_add" event.

    # The callback used for the "on_raw_reaction_add" event.
    async def on_reaction(self, payload):
        # Checks to make sure the bot can post in the channel or if the user ID is the bot's user ID.
        if payload.channel_id not in config.BOT_CHANNEL_IDS or payload.user_id == self.bot_client.user.id:
            return
            
        msg_id = payload.message_id # Grabs the message ID.
        channel_id = payload.channel_id # Grabs the channel ID.
        channel: discord.TextChannel = self.bot_client.get_channel(channel_id) # Gets the text channel object using the channel ID.

        split_reroll = config.REROLL_REACTION.split(':') # Splits the re-roll reaction with ":".

        # Checks if the re-roll reaction is a default reaction.
        if payload.emoji.id == None:
            # Checks if the split list of the emoji is equal to 1.
            if len(split_reroll) == 1:
                emoji_flag = payload.emoji.name == config.REROLL_REACTION # Set's the emoji flag to True if the name of the emoji is equal to the re-roll reaction.

            # Checks if the split list of the emoji is equal to 3.
            elif len(split_reroll) == 3:
                names_match = payload.emoji.name.lower() == config.REROLL_REACTION.split(':')[1].lower() #  Checks if the name of the emoji is the same as the re-roll reaction name.
                ids_match = payload.emoji.id == int(config.REROLL_REACTION.split(':')[2]) # Checks if the id of the emoji is the same as the re-roll ID.
                emoji_flag =  names_match and ids_match # Creates a flag from the two previous flags.
        else:
            # Checks if the split list of the emoji is equal to 1.
            if len(split_reroll) == 1:
                emoji_flag = False # Sets the emoji flag to False.
            else:
                names_match = payload.emoji.name.lower() == config.REROLL_REACTION.split(':')[1].lower() # Checks if the names of the emoji is equal to the name of the re-roll reaction.
                ids_match = payload.emoji.id == int(config.REROLL_REACTION.split(':')[2]) # Checks if the IDs of the emoji is equal to the name of the re-roll ID.
                emoji_flag =  names_match and ids_match # Creates a flag from the two previous flags.

        # Checks if the emoji flag is False and returns if so.
        if not emoji_flag:
            return

        reroll_info = self.get_reroll_message(msg_id) # Retrieves re-roll message from message id.
        success = reroll_info[0] # Checks if the retrieval was a success.
        role = reroll_info[1] # Gets the re-roll type.

        # If the retreival failed the function returns.
        if not success:
            return

        # Checks if the roll type is damage.
        if role == ReRollTypes.DAMAGE:
            await self.reroll_damage(channel) # Calls reroll_damage function.

        # Checks if the roll type is healer.
        elif role == ReRollTypes.HEALER:
            await self.reroll_healers(channel) # Calls reroll_healers function.
        
        # Checks if the roll type is tank.
        elif role == ReRollTypes.TANK:
            await self.reroll_tank(channel) # Calls reroll_tank function.

        # Check if the roll type is team.
        elif role == ReRollTypes.TEAM:
            await self.reroll_team(channel) # Calls the reroll_team function.

    # Gets a message if it's a re-roll message, otherwise it returns None.
    def get_reroll_message(self, id):
        team_available = len(self.previous_team) != 0 # Checks if the team role is available for re-roll.
        
        # Creates a flag to see if there are re-roll messages available.
        is_reroll_msg = team_available and self.previous_team[0] == id or self.damage_available and self.previous_damage[0] == id or self.healers_available and self.previous_healers[0] == id or self.tanks_available and self.previous_tanks[0] == id

        # Returns False if there are re-roll messages available.
        if not is_reroll_msg:
            return tuple([False, None])

        # Creates a list from the previous called commands.
        reroll_info = [self.previous_damage, 
                    self.previous_healers, 
                    self.previous_tanks, 
                    self.previous_team]
        reroll_info = [item for item in reroll_info if len(item) == 3 and item[0] == id] # Filters re-roll information.
        reroll_info = reroll_info[0] # Stores the first index as the variable.

        # Returns False if the re-roll information doesn't have all three elements.
        if len(reroll_info) != 3:
            return tuple([False, None])

        return tuple([True, reroll_info[1]]) # Returns re-roll message.
    
    @property
    def damage_available(self):
        return len(self.previous_damage) == 3 # Checks if damage re-roll is available.

    @property
    def tanks_available(self):
        return len(self.previous_tanks) == 3 # Checks if tank re-roll is available.

    @property
    def healers_available(self):
        return len(self.previous_healers) == 3 # Checks if healer re-roll is available.

    @property
    def team_available(self):
        return len(self.previous_team) == 3 # Checks if team re-roll is available.

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
        

        @SCCommand(name = 'team', category = 'Role Picker', description = 'Give {} player names and it\'ll spit out their roles.'.format(max_player_count), example = 'team {name 1} {name 2} {name...} {name 6}')
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

