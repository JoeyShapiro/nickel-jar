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

# load token from env
discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    print("DISCORD_TOKEN not found", flush=True)
    exit(1)

# load all word lists in memory (ext is txt)
words = []
for file in os.listdir(f'{data_path}/'):
    if file.endswith('.txt'):
        with open(f'{data_path}/{file}', 'r') as f:
            for line in f:
                words.append(line.strip())
print(f"Loaded {len(words)} word(s)", flush=True)

time.sleep(10)
conn = mysql.connector.connect(
    host="db",
    user="admin",
    password="toor",
    database="nickeljar",
    autocommit=True
)

# This example requires the 'message_content' intent.

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
handler = logging.FileHandler(filename=f'{data_path}/discord.log', encoding='utf-8', mode='a')

# client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}', flush=True)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    if message.author == bot.user:
        return

    content = message.content.lower()
    # remove punctuation
    content = ''.join(e for e in content if e.isalnum() or e.isspace())
    vulgarity = {}
    for word in content.split():
        if word in words:
            await message.channel.send(f"{message.author} added a nickel to the jar")
            # add_nickel(message)
            vulgarity[word] = vulgarity.get(word, 0) + 1
    
    # round about way, but it works out
    cursor = conn.cursor()
    for word, count in vulgarity.items():
        # oh lol. would only add once for each word
        for _ in range(count):
            cursor.execute("insert into nickels (guild, username, word) VALUES (%s, %s, %s)",
                           (message.guild.name, message.author.name, word)
                          )
    cursor.close()

@bot.hybrid_command(
    name="word_list",
    description="Get the number of words in the list",
)
async def word_list(ctx):
    print(f"word_list called by {ctx.author.name}", flush=True)
    await ctx.send(f"Loaded {len(words)} word(s)")

@bot.hybrid_command(
    name="summary",
    description="Summarize the nickels you've added",
)
async def summary(ctx, censor: bool=False, cross_guild: bool=False):
    print(f"summary called by {ctx.author.name}", flush=True)
    cursor = conn.cursor()
    stmt = f"select word, count(*) from nickels where username=%s {'and guild=%s' if cross_guild else ''} group by word"
    params = (ctx.author.name,) if not cross_guild else (ctx.author.name, ctx.guild.name)
    cursor.execute(stmt, params)
    rows = cursor.fetchall()
    cursor.close()
    
    nickels = 0
    messages = [  ]
    for word, count in rows:
        if censor:
            # convert word to a** format
            censored = word[0] + ('\*' * (len(word)-1))
        messages.append(f"{censored if censor else word}: {count}")
        nickels += count
    
    # add message to the beginning of the list
    messages = [f"There are {nickels} nickels in the jar"] + messages
    messages.append(f"{ctx.author.name} has donated ${(nickels*0.05):.2f}")
    
    await ctx.send('\n'.join(messages))

bot.run(discord_token, log_handler=handler, log_level=logging.INFO)
