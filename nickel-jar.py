import json
import discord
from discord.ext import commands
import logging
import os
import mysql.connector
import time

# print version of discord.py
print(discord.__version__)

data_path = 'data'

with open(f'{data_path}/secrets.json', 'r') as f:
    content = f.read()
    secrets = json.loads(content)

# load all word lists in memory (ext is txt)
words = []
for file in os.listdir(f'{data_path}/'):
    if file.endswith('.txt'):
        with open(f'{data_path}/example.txt', 'r') as f:
            for line in f:
                words.append(line.strip())
print(f"Loaded {len(words)} word(s)", flush=True)

time.sleep(10)
conn = mysql.connector.connect(
    host="db",
    user="admin",
    password="toor",
    database="nickeljar"
)

print(conn)

# This example requires the 'message_content' intent.

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
handler = logging.FileHandler(filename=f'{data_path}/discord.log', encoding='utf-8', mode='a')

# client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}', flush=True)

@bot.event
async def on_message(message):
    print(message.content, flush=True)
    await bot.process_commands(message)
    
    if message.author == bot.user:
        return

    content = message.content.lower()
    # remove punctuation
    content = ''.join(e for e in content if e.isalnum() or e.isspace())
    for word in content.split():
        if word in words:
            await message.channel.send(f"{message.author} added a nickel to the jar")

@bot.command()
async def word_list(ctx):
    await ctx.send(f"Loaded {len(words)} word(s)")

@bot.command()
async def summary(ctx):
    await ctx.send(f"Nickel jar has {len(words)} nickel(s)")

bot.run(secrets['discord-token'], log_handler=handler, log_level=logging.INFO)
