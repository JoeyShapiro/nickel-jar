import json
import discord
from discord.ext import commands
import logging
import os

with open('server/secrets.json', 'r') as f:
    content = f.read()
    secrets = json.loads(content)

# load all word lists in memory (ext is txt)
words = []
for file in os.listdir('server/'):
    if file.endswith('.txt'):
        with open('server/example.txt', 'r') as f:
            for line in f:
                words.append(line.strip())
print(f"Loaded {len(words)} word(s)", flush=True)

# This example requires the 'message_content' intent.

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
handler = logging.FileHandler(filename='server/discord.log', encoding='utf-8', mode='a')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}', flush=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()
    # remove punctuation
    content = ''.join(e for e in content if e.isalnum() or e.isspace())
    for word in content.split():
        if word in words:
            await message.channel.send(f"{message.author} added a nickel to the jar")

client.run(secrets['discord-token'], log_handler=handler, log_level=logging.INFO)
