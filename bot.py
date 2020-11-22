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

with open('themes.csv') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        advent_calendar[line[0]] = line[1]


channel_ids = []

@aiocron.crontab('0 5 * * *')
async def cronjob1():
    today = datetime.date.today().strftime('%Y-%m-%d')
    theme = advent_calendar[today]
    for channel_id in channel_ids:
        await client.get_channel(channel_id).send(f"Today's theme is {theme}")

@client.event
async def on_ready():
    global channel_ids
    for guild in client.guilds:
        print(f'{client.user} has connected to Discord server {guild}!')
        for channel in guild.channels:
            if channel.name == 'music':
                channel_ids.append(channel.id)

client.run(TOKEN)
