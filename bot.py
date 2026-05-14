import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import random
import os

# Load token and weather key from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

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
@bot.command(name='8ball')
async def ball8(ctx, *, question):
    responses = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Do not count on it.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.',
    ]
    answer = random.choice(responses)
    await ctx.send(f'Question: {question}\nAnswer: **{answer}**')

# !weather [city] - fetches live weather for a given city
@bot.command()
async def weather(ctx, *, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data['cod'] != 200:
        await ctx.send(f'City not found. Please check the spelling and try again.')
        return

    name = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']

    await ctx.send(
        f'🌤️ **Weather in {name}, {country}**\n'
        f'🌡️ Temperature: **{temp}°C** (feels like {feels_like}°C)\n'
        f'☁️ Condition: **{description}**\n'
        f'💧 Humidity: **{humidity}%**'
    )

# Run the bot
bot.run(TOKEN)