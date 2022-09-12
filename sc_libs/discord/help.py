import discord
from sc_libs.discord.command_class import Command_Class
from sc_libs.discord.command import Command


class SCHelp(Command_Class):
    help_thumbnail = 'https://upload.wikimedia.org/wikipedia/commons/b/b9/1328101905_Help.png'
    help_color = 0x0096FF
    command_color = 0x800080

    def __init__(self, client):
        client.remove_command('help')  # Removes the default help command.
        super().__init__(client)


    def load_commands(self):

        @Command(name='help', example='help {optional: Command Name}', description='Returns info on the bot commands.', aliases=['commands'], argumentDescriptions=['Command Name: The name of the command you want to more info on.'])
        @self.client.command(aliases=['commands'])
        async def help(ctx, commandName=None):  # New help command.
            channelName = ctx.channel.name  # Gets the channel name.
            if ('bot' not in channelName):
                return  # Returns if "bot" isn't in the channel name.

            if (commandName == None):
                embed = self.build_help_embed(ctx)  # Builds the help embed.
                # Creates a webhook and sends the created embed.
                await ctx.send(embed=embed)

            else:
                embed, success = self.build_command_help_embed(commandName)
                if (success):
                    await ctx.send(embed=embed)

                else:
                    embed = self.build_help_embed(ctx)
                    await ctx.send(embed=embed)
    @classmethod
    def set_thumbnail(self, url: str):
        self.help_thumbnail = url
    @classmethod
    def set_colors(self, h_color=None, c_color=None):
        """Sets the colors for the help embed and command embed.

        Properties
        ----------
        h_color: `int`
            The color for the help command embed.
        
        c_color: `int`
            The color for the help command embed.
        """
        if (h_color != None):
            self.help_color = h_color

        if (c_color != None):
            self.command_color = c_color

    @classmethod
    def build_help_embed(self, ctx):
        """Builds and returns an embed with all the help information needed.

        Properties
        -----------
        ctx: `discord.ext.commands.Context`
            The context of the discord command.
        """
        embed = discord.Embed(
            title=':question: Bot Commands', color=self.help_color)
        embed.set_thumbnail(url=self.help_thumbnail)
        #embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        categoryString = "```fix"

        # Loops through all categories.
        for category in Command.categories:
            categoryString += '\n- {0}'.format(category)

        categoryString += "```"
        embed.add_field(name='Categories', value=categoryString, inline=True)
        embed.add_field(name='Prefix', value='```{0}```'.format(
            Command.prefix), inline=True)

        # Loops through all categories
        for category in Command.categories:
            appendedString = ''

            # Loops through all commands
            for command in Command.commandList:
                aliases = ''
                if (command.aliases != None):
                    aliases = '\n`Aliases: {0}`'.format(
                        ', '.join(command.aliases))
                if (command.category == category):
                    appendedString += '\n**{0.name}** {2} \n`Ex: {1}{0.example}`\n```json\n"Description: {0.description}"```'.format(
                        command, Command.prefix, aliases)

            embed.add_field(name=':information_source: {0} Commands'.format(category), value=appendedString, inline=False)

        return embed

    @classmethod
    def build_command_help_embed(self, commandName):
        """Builds and returns an embed of the given command.

        Properties
        -----------
        commandName: `string`
            The name of the command you want to build a help embed for.
        """
        tempCommand = None
        for command in Command.commandList:
            if (command.name == commandName):
                tempCommand = command
                break

            if (command.aliases != None and commandName in command.aliases):
                tempCommand = command
                break

        if (tempCommand == None):
            return (None, False)

        embed = discord.Embed(title=':question: Command Info', color=self.command_color)
        embed.set_thumbnail(url=self.help_thumbnail)
        embed.add_field(name='Name', value=tempCommand.name)
        embed.add_field(name='Category', value=tempCommand.category)

        if (tempCommand.aliases != None):
            embed.add_field(name='Aliases', value=', '.join(tempCommand.aliases))

        embed.add_field(name='Example', value='{0}{1}'.format(Command.prefix, tempCommand.example), inline=False)
        embed.add_field(name='Description', value=tempCommand.description)
        if (tempCommand.argumentDescriptions != None):
            argDesc = ""
            for arg in tempCommand.argumentDescriptions:
                argDesc += '```{0}```\n'.format(arg)

            embed.add_field(name="Argument Descriptions", value=argDesc, inline=False)

        return (embed, True)