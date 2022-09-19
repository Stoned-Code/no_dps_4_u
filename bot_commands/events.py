import abc
import discord
from bot_commands.enums.Roles import Role
from bot_commands.role_picker import RolePicker
import config
from discord.ext.commands import Bot

def register_events(client: Bot, role_picker: RolePicker):
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

        if payload.channel_id not in config.BOT_CHANNEL_IDS or payload.user_id == client.user.id:
            return
            
        msg_id = payload.message_id
        channel_id = payload.channel_id
        channel: discord.TextChannel = client.get_channel(channel_id)

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

        reroll_info = role_picker.get_reroll_message(msg_id)
        success = reroll_info[0]
        role = reroll_info[1]

        if not success:
            return

        if role == Role.DAMAGE:
            await role_picker.reroll_damage(channel)

        elif role == Role.HEALER:
            await role_picker.reroll_healers(channel)
        
        elif role == Role.TANK:
            await role_picker.reroll_tank(channel)
        