'''
PO(I)TD

A Discord bot that sends a random OI problem every day
'''

import os
import asyncio
from datetime import datetime, timedelta

import requests
import discord
from discord.ext import commands, tasks

TOKEN = os.environ['DISCORD_TOKEN']

BOT = commands.Bot("$")


async def random_problem(description, channel):
    '''
    Gets a random problem from APIOIPA and sends it as an embed
    '''

    print('Sending problem!')
    problem = requests.get('https://apioipa.herokuapp.com/random-problem/').json()

    embed = discord.Embed(
        title=f'{problem["source"]["abbreviation"]} {problem["from_year"]} - {problem["name"]}',
        color=0x00ff00,
        description=description,
        url=problem['url']
    )
    embed.set_image(url=problem['image'])

    await channel.send(embed=embed)


@BOT.command()
async def gimme(ctx):
    '''
    Sends a random problem to the user in the channel where the command was sent
    '''

    await random_problem('Random Problem', ctx.message.channel)


@tasks.loop(hours=24)
async def potd():
    '''
    Sends a random problem every day
    '''

    await random_problem('Problem of the Day', BOT.get_channel(int(os.environ['CHANNEL_ID'])))


@potd.before_loop
async def before_potd():
    '''
    Makes sure the bot sends a random problem every day at 0:00 UTC
    '''

    await BOT.wait_until_ready()

    hour = 15
    minute = 3
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, hour, minute)

    if now.hour >= hour and now.minute > minute:
        future += timedelta(days=1)

    await asyncio.sleep((future - now).seconds)


@BOT.event
async def on_ready():
    '''
    Called when the bot is ready
    '''

    print(f'{BOT.user} has connected to Discord!')


potd.start()

BOT.run(TOKEN)
