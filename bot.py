"""
PO(I)TD

A Discord bot that sends a random OI problem every day
"""

import os
import logging

from discord import Activity, ActivityType
from discord.ext.commands import Bot, when_mentioned_or

from cogs.bot_info import BotInfo
from cogs.problems import Problems

logging.basicConfig(level=logging.INFO)

prefix = '$'
if 'BOT_PREFIX' in os.environ:
    prefix = os.environ['BOT_PREFIX']

bot = Bot(
    command_prefix=when_mentioned_or(prefix),
    help_command=None,
    activity=Activity(type=ActivityType.watching, name='you solve problems')
)

bot.add_cog(BotInfo(bot))
bot.add_cog(Problems(bot))

bot.run(os.environ['DISCORD_TOKEN'])
