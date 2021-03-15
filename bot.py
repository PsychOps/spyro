import discord
import config
import aiohttp
import psutil
import traceback
import logging
from discord.ext import commands
from discord_slash import SlashCommand
logging.basicConfig(level=logging.INFO)

bot = commands.AutoShardedBot(
    command_prefix=commands.when_mentioned_or('sp!'),
    case_insensitive=True,
    case_insensitive_prefix=True,
    allowed_mentions=discord.AllowedMentions.none(),
    max_messages=10000,
    intents=discord.Intents.all(),
#    owner_ids=[698080201158033409, 443217277580738571],
    status=discord.Status.dnd,
    activity=discord.Activity(type=discord.ActivityType.playing, name='sp!help'),
    description="A very cool discord bot for your server!"
)
slash = SlashCommand(client=bot, sync_commands=True, override_type=True, sync_on_cog_reload=True)

@bot.event
async def on_ready():
    print(f'\n-= {bot.name} has started successfully =-\n')

for extension in config.extensions:
    try:
        bot.load_extension(extension)
        print(f'[extension] {extension} was loaded successfully!')
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tbe = "".join(tb) + ""
        print(f'[WARNING] Could not load extension {extension}: {tbe}')

bot.run(config.token) # https://discord.com/api/oauth2/authorize?client_id=805872242184683551&permissions=2117988087&scope=bot
