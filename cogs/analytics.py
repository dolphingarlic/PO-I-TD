"""
Cog that gives information about the bot
"""

import os
from datetime import datetime

import discord
from discord.ext.commands import Cog, command
import prismapy


class Analytics(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.analytics = prismapy.Prismalytics(os.environ['PRISMA_TOKEN'], bot, save_server=True)

    @Cog.listener()
    async def on_command(self, ctx):
        await self.analytics.send(ctx)
