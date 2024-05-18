import json
import discord
from discord.ext import commands
import logging

with open('server/secrets.json', 'r') as f:
    content = f.read()
    secrets = json.loads(content)

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
    print(f'{message.author} said {message.content}, {message}', flush=True)
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(secrets['discord-token'], log_handler=handler, log_level=logging.INFO)
