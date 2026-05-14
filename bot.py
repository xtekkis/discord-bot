import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import random
import os

# Load token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up the bot with a command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Runs when the bot successfully connects to Discord
@bot.event
async def on_ready():
    print(f'{bot.user} is online and ready!')

# !hello - greets the user
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}! I am Utilix, your utility bot. Type !help to see what I can do!')

# !ping - checks response time
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! 🏓 Response time: {latency}ms')

# !joke - fetches a random joke from an API
@bot.command()
async def joke(ctx):
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    data = response.json()
    await ctx.send(f'{data["setup"]}\n\n||{data["punchline"]}||')

# !8ball - magic 8 ball, answers a question randomly
@bot.command()
async def ball8(ctx, *, question):
    responses = [
        'It is certain.',
        'Without a doubt.',
        'Yes definitely.',
        'Most likely.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Cannot predict now.',
        'Do not count on it.',
        'My reply is no.',
        'Outlook not so good.',
        'Very doubtful.',
    ]
    answer = random.choice(responses)
    await ctx.send(f'🎱 Question: {question}\nAnswer: **{answer}**')

# Run the bot
bot.run(TOKEN)