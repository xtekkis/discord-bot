import discord
from discord.ext import commands
from dotenv import load_dotenv
import html
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
bot.remove_command('help')

# Runs when the bot successfully connects to Discord
@bot.event
async def on_ready():
    print(f'{bot.user} is online and ready!')

# !hello greets the user
@bot.command()
async def hello(ctx):
    embed = discord.Embed(
        title='👋 Hello!',
        description=f'Hi {ctx.author.name}! I am Utilix, your utility bot. Type !help to see what I can do!',
        color=0x7289da
    )
    embed.set_footer(text='Utilix Bot')
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

# !ping checks response time
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title='🏓 Pong!',
        description=f'Response time: **{latency}ms**',
        color=0x2ecc71
    )
    embed.set_footer(text='Utilix Bot')
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

# !joke fetches a random joke from an API
@bot.command()
async def joke(ctx):
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    data = response.json()
    embed = discord.Embed(
        title='😂 Random Joke',
        color=0xf1c40f
    )
    embed.add_field(name='Setup', value=data['setup'], inline=False)
    embed.add_field(name='Punchline', value=f'||{data["punchline"]}||', inline=False)
    embed.set_footer(text='Utilix Bot')
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

# !8ball magic 8 ball, answers a question randomly
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
    embed = discord.Embed(
        title='🎱 Magic 8 Ball',
        color=0x9b59b6
    )
    embed.add_field(name='Question', value=question, inline=False)
    embed.add_field(name='Answer', value=f'**{answer}**', inline=False)
    embed.set_footer(text='Utilix Bot')
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

# !weather [city] fetches live weather for a given city
@bot.command()
async def weather(ctx, *, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data['cod'] != 200:
        embed = discord.Embed(
            title='❌ City Not Found',
            description='Please check the spelling and try again.',
            color=0xe74c3c
        )
        embed.set_footer(text='Utilix Bot')
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)
        return
    name = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    embed = discord.Embed(
        title=f'🌤️ Weather in {name}, {country}',
        color=0x3498db
    )
    embed.add_field(name='🌡️ Temperature', value=f'**{temp}°C** (feels like {feels_like}°C)', inline=False)
    embed.add_field(name='☁️ Condition', value=f'**{description}**', inline=False)
    embed.add_field(name='💧 Humidity', value=f'**{humidity}%**', inline=False)
    embed.set_footer(text='Utilix Bot')
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

# !coinflip flips a coin
@bot.command()
async def coinflip(ctx):
    result = random.choice(['Heads', 'Tails'])
    embed = discord.Embed(
        title='🪙 Coin Flip',
        description=f'The coin landed on **{result}!**',
        color=0xe67e22
    )
    embed.set_footer(text='Utilix Bot')
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

# !roll [number] rolls a dice with the given number of sides
@bot.command()
async def roll(ctx, sides: int = 6):
    if sides < 2:
        embed = discord.Embed(
            title='❌ Invalid Number',
            description='Please enter a number greater than 1.',
            color=0xe74c3c
        )
        embed.set_footer(text='Utilix Bot')
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)
        return
    result = random.randint(1, sides)
    embed = discord.Embed(
        title='🎲 Dice Roll',
        description=f'You rolled a **{result}** out of {sides}!',
        color=0xe67e22
    )
    embed.set_footer(text='Utilix Bot')
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

# !poll [question] [option1] [option2] creates a poll with reactions
@bot.command()
async def poll(ctx, question, option1, option2):
    embed = discord.Embed(
        title='📊 Poll',
        description=f'**{question}**',
        color=0x1abc9c
    )
    embed.add_field(name='🅰️ Option 1', value=option1, inline=True)
    embed.add_field(name='🅱️ Option 2', value=option2, inline=True)
    embed.set_footer(text='Utilix Bot')
    embed.timestamp = discord.utils.utcnow()
    message = await ctx.send(embed=embed)
    await message.add_reaction('🅰️')
    await message.add_reaction('🅱️')

# !trivia fetches a random trivia question with multiple choice answers
@bot.command()
async def trivia(ctx):
    response = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
    data = response.json()['results'][0]

    question = html.unescape(data['question'])
    correct = html.unescape(data['correct_answer'])
    wrong = [html.unescape(ans) for ans in data['incorrect_answers']]

    # Combine and shuffle all answers
    options = wrong + [correct]
    random.shuffle(options)

    # Label options as A, B, C, D
    labels = ['🇦', '🇧', '🇨', '🇩']
    answer_text = '\n'.join([f'{labels[i]} {options[i]}' for i in range(len(options))])
    correct_label = labels[options.index(correct)]

    embed = discord.Embed(
        title='🧠 Trivia Time!',
        description=question,
        color=0xe91e63
    )
    embed.add_field(name='Options', value=answer_text, inline=False)
    embed.set_footer(text='Utilix Bot • Reply with A B C or D')
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

    # Wait for a response from the same user in the same channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', timeout=20.0, check=check)
        user_answer = msg.content.strip().upper()

        correct_letters = {'🇦': 'A', '🇧': 'B', '🇨': 'C', '🇩': 'D'}
        correct_letter = correct_letters.get(correct_label, '')

        if user_answer == correct_letter:
            result_embed = discord.Embed(
                title='✅ Correct!',
                description=f'Well done {ctx.author.name}! The answer was **{correct}**',
                color=0x2ecc71
            )
        else:
            result_embed = discord.Embed(
                title='❌ Wrong!',
                description=f'The correct answer was **{correct}**',
                color=0xe74c3c
            )
        result_embed.set_footer(text='Utilix Bot')
        result_embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=result_embed)

    except:
        timeout_embed = discord.Embed(
            title='⏰ Time is up!',
            description=f'The correct answer was **{correct}**',
            color=0xe74c3c
        )
        timeout_embed.set_footer(text='Utilix Bot')
        timeout_embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=timeout_embed)

# !help shows all available commands
@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title='📖 Utilix Commands',
        description='Here are all the available commands:',
        color=0x7289da
    )
    embed.add_field(
        name='🔧 Utility',
        value='`!hello` Greet the bot\n`!ping` — Check response time',
        inline=False
    )
    embed.add_field(
        name='🎮 Fun',
        value='`!joke` Get a random joke\n`!8ball <question>` — Ask the magic 8 ball\n`!coinflip` — Flip a coin\n`!roll <sides>` — Roll a dice',
        inline=False
    )
    embed.add_field(
        name='🌍 Info',
        value='`!weather <city>` Get live weather',
        inline=False
    )
    embed.add_field(
        name='🎯 Games',
        value='`!trivia` Answer a trivia question\n`!poll <question> <option1> <option2>` — Create a poll',
        inline=False
    )
    embed.set_footer(text='Utilix Bot')
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)