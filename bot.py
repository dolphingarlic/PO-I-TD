import os
import asyncio

from datetime import datetime, timedelta
import requests
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

BOT = commands.Bot("$")
CHANNEL = None


@tasks.loop(hours=24)
async def random_problem():
    print('Sending problem!')
    global CHANNEL
    problem = requests.get('https://apioipa.herokuapp.com/random-problem/').json()
    source = requests.get(f'https://apioipa.herokuapp.com/sources/{problem["source"]}').json()['abbreviation']

    embed = discord.Embed(title=f'{source} {problem["from_year"]} - {problem["name"]}', color=0x00ff00)
    embed.url = problem['url']
    embed.description = 'Problem of the Day'
    embed.set_image(url=problem['image'])

    await CHANNEL.send(embed=embed)


@random_problem.before_loop
async def before_random_problem():
    await BOT.wait_until_ready()

    hour = 8
    minute = 20
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, hour, minute)

    if now.hour >= hour and now.minute > minute:
        future += timedelta(days=1)

    await asyncio.sleep((future - now).seconds)


@BOT.event
async def on_ready():
    print(f'{BOT.user} has connected to Discord!')
    global CHANNEL
    CHANNEL = BOT.get_channel(627064201797697543)


random_problem.start()

BOT.run(TOKEN)
