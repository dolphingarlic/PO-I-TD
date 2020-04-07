import os

import requests
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

BOT = commands.Bot("~")
CHANNEL = None


@BOT.event
async def on_ready():
    print(f'{BOT.user} has connected to Discord!')


@tasks.loop(hours=24)
async def random_problem():
    global CHANNEL
    problem = requests.get(
        'https://apioipa.herokuapp.com/random-problem/').json()
    source = requests.get(
        f'https://apioipa.herokuapp.com/sources/{problem["source"]}').json()['abbreviation']

    embed = discord.Embed(
        title=f'{source} {problem["from_year"]} - {problem["name"]}', color=0x00ff00)
    embed.url = problem['url']
    embed.description = 'Problem of the Day'
    embed.set_image(url=problem['image'])

    await CHANNEL.send(embed=embed)


@BOT.command()
async def start(ctx):
    global CHANNEL
    if CHANNEL == None:
        CHANNEL = ctx.message.channel
        await ctx.send('Starting. You will be sent a random OI problem every day now.')
        random_problem.start()
    else:
        await ctx.send('The BOT is already running in another channel')


@BOT.command()
async def stop(ctx):
    global CHANNEL
    CHANNEL = None
    await ctx.send('Stopping BOT. You will no longer be sent random problems every day.')
    random_problem.stop()

BOT.run(TOKEN)
