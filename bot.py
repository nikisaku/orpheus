# bot.py
import aiocron
import csv
import datetime
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

advent_calendar = {}
trivia = {}

with open('themes.csv') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        advent_calendar[line[0]] = line[1]

with open('webaccesibility.csv') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        trivia[line[0]] = line[1]


channel_ids = []
trivia_channel_ids = []

@aiocron.crontab('0 5 * * *')
async def cronjob1():
    today = datetime.date.today().strftime('%Y-%m-%d')
    theme = advent_calendar[today]
    for channel_id in channel_ids:
        await client.get_channel(channel_id).send(f"Today's theme is {theme}")

@aiocron.crontab('0 8 * * *')
async def cronjob2():
    today = datetime.date.today().strftime('%Y-%m-%d')
    trivia_of_the_day = trivia[today]
    for channel_id in trivia_channel_ids:
        await client.get_channel(channel_id).send(trivia_of_the_day)

@client.event
async def on_ready():
    global channel_ids
    for guild in client.guilds:
        print(f'{client.user} has connected to Discord server {guild}!')
        for channel in guild.channels:
            if 'music' in channel.name:
                channel_ids.append(channel.id)
            if 'ciekawostka-dnia' in channel.name:
                trivia_channel_ids.append(channel.id)

client.run(TOKEN)
