"""
Cog that gives information about the bot
"""

import os
from datetime import datetime

import discord
from discord.ext.commands import Cog, command


class BotInfo(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

        self.prefix = '$'
        if 'BOT_PREFIX' in os.environ:
            self.prefix = os.environ['BOT_PREFIX']

    @command(aliases=['source'])
    async def github(self, ctx):
        """
        Sends the link to the bot's GitHub repo
        """

        await ctx.send('https://github.com/dolphingarlic/PO-I-TD')

    @command(aliases=['stats'])
    async def about(self, ctx):
        """
        Sends information about the bot
        """

        info = await self.bot.application_info()
        embed = discord.Embed(
            title=f'{info.name}',
            description=f'{info.description}',
            colour=0x1aaae5,
        ).add_field(
            name='Guild Count',
            value=len(self.bot.guilds),
            inline=True
        ).add_field(
            name='User Count',
            value=len(self.bot.users),
            inline=True
        ).add_field(
            name='Uptime',
            value=f'{datetime.now() - self.start_time}',
            inline=True
        ).add_field(
            name='Latency',
            value=f'{round(self.bot.latency * 1000, 2)}ms',
            inline=True
        ).set_footer(text=f'Made by {info.owner}', icon_url=info.owner.avatar_url)

        await ctx.send(embed=embed)

    @command()
    async def help(self, ctx):
        """
        Sends a help message
        """

        embed = discord.Embed(
            title='Help',
            description='PO(I)TD automatically sends a problem to a channel named `#problem-of-the-day` or `#potd` every day',
            colour=0x41c03f
        ).add_field(
            name=f'`{self.prefix}gimme`',
            value='Sends a random problem',
            inline=True
        ).add_field(
            name=f'`{self.prefix}about` or `{self.prefix}stats`',
            value='About PO(I)TD',
            inline=True
        ).add_field(
            name=f'`{self.prefix}invite` or `{self.prefix}topgg`',
            value='Bot invite link',
            inline=True
        ).add_field(
            name=f'`{self.prefix}help`',
            value='Shows this message',
            inline=True
        ).add_field(
            name=f'`{self.prefix}ping`',
            value='Check the bot\'s latency',
            inline=True
        ).add_field(
            name=f'`{self.prefix}github` or `{self.prefix}source`',
            value='Links to the bot\'s GitHub repo',
            inline=True
        )

        await ctx.send(embed=embed)

    @command(aliases=['topgg'])
    async def invite(self, ctx):
        """
        Sends a bot invite link
        """

        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=696993851574845581&permissions=52224&scope=bot')

    @command()
    async def ping(self, ctx):
        """
        Checks latency
        """

        await ctx.send(f'Pong; {round(self.bot.latency * 1000, 2)}ms')

    @Cog.listener()
    async def on_guild_join(self, guild):
        """
        Sends a nice message when added to a new server
        """

        embed = discord.Embed(
            title='Thanks for adding me to your server! :heart:',
            description=f'To get started, create a channel named `#problem-of-the-day` or `#potd`, or type `{self.prefix}help` for a list of commands',
            colour=0x2ac99e
        ).add_field(
            name='Contribute',
            value='We gladly accept contributions. To get started, ' +
            'check out [PO(I)TD\'s GitHub repo](https://github.com/dolphingarlic/PO-I-TD)',
            inline=False
        ).add_field(
            name='Have fun!',
            value=':zap:',
            inline=False
        )
        await guild.system_channel.send(embed=embed)
