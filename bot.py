import discord
import config
import aiohttp
import psutil
import traceback
import logging
from discord.ext import commands

"""logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)"""# Make it a little simpler to just log it to console for right now since everything is breaking e.e
logging.basicConfig(level=logging.INFO)

#  bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))

bot = commands.Bot(command_prefix=commands.when_mentioned_or('sp!'), case_insensitive=True, allowed_mentions=discord.AllowedMentions.none(), max_messages=10000, intents=discord.Intents.default())

@bot.event  # sets the bot status and prints when it has started in console with stats, stats include: The amount of users that are in the total amount of guilds and the discord.py version
async def on_ready():
    activity = discord.Game(name='sp!help', type=1)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('\n-= spyro has started successfully =-\n')

print('Test 2 works')
for extension in config.extensions:
    try:
        bot.load_extension(extension)
        print(f'[extension] {extension} was loaded successfully!')
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tbe = "".join(tb) + ""
        print(f'[WARNING] Could not load extension {extension}: {tbe}')

print('Test 3 works')

bot.run(config.token)
