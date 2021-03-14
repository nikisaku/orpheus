# bot.py
import aiocron
import csv
import datetime
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
VERIFICATION_MESSAGE_ID = 820693368182013952
VERIFICATION_ROLE_ID = 820690464100581377

client = discord.Client()

advent_calendar = {}
trivia = {}

with open('themes.csv') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        advent_calendar[line[0]] = line[1]

files_to_read = ['webaccessibility.csv', 'photography.csv', 'music.csv']
for file_to_read in files_to_read:
    with open(file_to_read) as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            trivia[line[0]] = line[1]

channel_ids = []
trivia_channel_ids = []
events_channel_ids = []
roles_channel_ids = []


@aiocron.crontab('15 5 * * *')
async def cronjob1():
    today = datetime.date.today().strftime('%Y-%m-%d')
    theme = advent_calendar[today]
    for channel_id in channel_ids:
        await client.get_channel(channel_id).send(f"Dzisiejszy temat to: {theme}")


@aiocron.crontab('0 7 * * *')
async def cronjob2():
    today = datetime.date.today().strftime('%Y-%m-%d')
    trivia_of_the_day = trivia[today]
    for channel_id in trivia_channel_ids:
        await client.get_channel(channel_id).send(trivia_of_the_day)


@aiocron.crontab('45 10 * * 2,4')
async def cronjob3():
    for channel_id in events_channel_ids:
        await client.get_channel(channel_id).send("Za kwadrans kawka na kanale głosowym Relaks! ☕")


@aiocron.crontab('0 11 * * 2,4')
async def cronjob4():
    for channel_id in events_channel_ids:
        await client.get_channel(channel_id).send("Zapraszamy na kanał głosowy Relaks na wspólną kawę! ☕")



def compare_emojis(reaction_emoji):
    return reaction_emoji.name == "🔑"

@client.event
async def on_raw_reaction_add(reaction):
    print("tutaj")
    print(reaction.emoji.name)
    if reaction.message_id != 820693368182013952:
        return
    if compare_emojis(reaction.emoji):
        verification_role = discord.utils.get(reaction.member.guild.roles, id=VERIFICATION_ROLE_ID)
        await reaction.member.add_roles(verification_role)
        print("role added")

@client.event
async def on_raw_reaction_remove(reaction):
    if reaction.message_id != 820693368182013952:
        return
    if compare_emojis(reaction.emoji):
        # guild_id + user_id -> member.id / member object
        guild = client.get_guild(reaction.guild_id)
        member = discord.utils.get(guild.members, id=reaction.user_id)
        # member = client.get_member(reaction.user_id)
        verification_role = discord.utils.get(guild.roles, id=VERIFICATION_ROLE_ID)
        await member.remove_roles(verification_role)
        print("role removed")

@client.event
async def on_ready():
    global channel_ids
    for guild in client.guilds:
        print(f'{client.user} has connected to Discord server {guild}!')
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                if 'music' in channel.name:
                    channel_ids.append(channel.id)
                if 'ciekawostka-dnia' in channel.name:
                    trivia_channel_ids.append(channel.id)
                if 'wydarzenia' in channel.name:
                    events_channel_ids.append(channel.id)
                if 'role' in channel.name:
                    roles_channel_ids.append(channel.id)
                    try:
                        msg = await channel.fetch_message(VERIFICATION_MESSAGE_ID)
                        print(msg.content)
                    except discord.NotFound:
                        # TODO zmień na coś lepszego
                        print("Wiadomość weryfikacyjna o tym ID nie istnieje")
                    # await client.get_channel(channel.id).send("bot is online")



client.run(TOKEN)
