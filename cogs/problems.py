"""
Cog that gives problems
"""

import asyncio
from datetime import datetime, timedelta

import aiohttp
from discord import Embed
from discord.utils import find
from discord.ext.commands import Cog, command
from discord.ext.tasks import loop


class Problems(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.potd.start()

    async def fetch(self, session, url, **kwargs):
        """
        Uses aiohttp to make http GET requests
        """

        async with session.get(url, **kwargs) as response:
            return await response.json()

    async def random_problem(self, description, channel):
        """
        Gets a random problem from APIOIPA and sends it as an embed
        """

        async with aiohttp.ClientSession() as session:
            problem = await self.fetch(
                session,
                'https://apioipa.herokuapp.com/random-problem/'
            )

        embed = Embed(
            title=f'{problem["source"]["abbreviation"]} {problem["from_year"]} - {problem["name"]}',
            color=0x00ff00,
            description=description,
            url=problem['url']
        )
        embed.set_image(url=problem['image'])

        await channel.send(embed=embed)

    # TODO: Add problem filters
    @command()
    async def gimme(self, ctx):
        """
        Sends a random problem to the user in the channel where the command was sent
        """

        await self.random_problem('Random Problem', ctx.message.channel)

    @loop(hours=24)
    async def potd(self):
        """
        Sends a random problem every day
        """

        for guild in self.bot.guilds:
            potd_channel = find(lambda x: x.name == 'problem-of-the-day' or x.name == 'potd', guild.text_channels)
            await self.random_problem('Problem of the Day', potd_channel)

    @potd.before_loop
    async def before_potd(self):
        """
        Makes sure the bot sends a random problem every day at 0:00 UTC
        """

        await self.bot.wait_until_ready()

        hour = 0
        minute = 0
        now = datetime.now()
        future = datetime(now.year, now.month, now.day, hour, minute)

        if now.hour >= hour and now.minute > minute:
            future += timedelta(days=1)

        await asyncio.sleep((future - now).seconds)
