import discord
from discord.ext import commands
from dotenv import load_dotenv
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

# Run the bot
bot.run(TOKEN)