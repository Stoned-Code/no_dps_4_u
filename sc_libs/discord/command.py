from os import name
import discord

from sc_libs.discord.command_class import Command_Class

class Command:
    """SC Command
    
    An object containg basic information about commands.

    Used for indexing command info.

    Static Variables
    -----------
    prefix: `string`
        Defaulted to "!".

        Change using `set_prefix` method.

    Methods
    -----------
    - set_prefix

    Arguments
    -----------
    name: :class: `string` (Required)
        Discord command name without prefix.

    description: :class: `string`
        The description that gives details about the command.

    example: :class: `string`
        The example command that's shown.
        Input without prefix.

    category: :class: `string`
        The category that the command is in.

    aliases: :class: `list[string]`
        The aliases used for the command.

    argumentDescriptions: :class: `string`
        The descriptions of the command's arguments.

    prefix: :class: `string`
        The prefix used for the commands
    """


    commandList = []
    categories = []
    prefix = '!'


    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description', "No description available.")
        self.example = kwargs.get('example', self.name)
        self.category = kwargs.get('category', "Default")
        self.aliases = kwargs.get('aliases', None)
        self.argumentDescriptions = kwargs.get('argumentDescriptions', None)

        Command.commandList.append(self)
        if (self.category != None and self.category not in Command.categories):
            Command.categories.append(self.category)


    def __call__(self, func):

        def decoration(**kwargs):
            return func

        return decoration


    def __str__(self):
        info = 'Name: {0.name}\nExample: {0.prefix}{0.example}\nCategory: {0.category}\nDescription: {0.description}'.format(self)
        return info


    @classmethod
    def arg_concatenate(self, *args, **kwargs):
        seperator = kwargs.get('seperator', ' ')
        try:
            conc = ''
            for arg in args:
                conc += '{0}{1}'.format(arg, seperator)

            return (conc, True)
        except Exception as ex:
            print('Something fucked up concatenating Kwargs: {0}'.format(ex))
            return ('', False)


    @classmethod
    def set_prefix(self, prefix):
        """Sets the prefix of the `SC_Command` class

        Properties
        -----------
        prefix: `string`
            The prefix used for the commands
        """
        self.prefix = prefix
