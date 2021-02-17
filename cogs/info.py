import discord, config, time, aiohttp
import psutil, platform
from collections import Counter
from discord.ext import commands

class info(commands.Cog, name="Info"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Bot's latency to discord")
    async def ping(self, ctx):
        """ See bot's latency to discord """
        discord_start = time.monotonic()
        self.bot.session = aiohttp.ClientSession(loop=self.bot.loop)
        async with self.bot.session.get("https://discord.com/") as resp:
            if resp.status == 200:
                discord_end = time.monotonic()
                discord_ms = f"{round((discord_end - discord_start) * 1000)}ms"
            else:
                discord_ms = "fucking dead"
        await ctx.send(f"\U0001f3d3 Pong   |   {discord_ms}")

    @commands.command(brief="test command")
    async def respond(self, ctx, *, args):
        e=discord.Embed(color=config.red)
        e.description = f"{args}"
        await ctx.send(embed=e)
    
    
    @commands.command(brief="Credit to others", alias="icon")
    async def credit(self, ctx):
        e = discord.Embed(color=config.blue)
        e.description = f"""
__**Graphics**__
`FLVincent 42` - Icon
╠ [Logo on wikimedia](https://commons.wikimedia.org/wiki/File:LOGO_Wolf_Games.jpg)
╚ Licensed under the: [cc-by-sa-4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en) license.
"""
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/808426270139351050/808426339082305567/LOGO_Wolf_Games.png")
        await ctx.send(embed=e)

    @commands.command(brief="bot info")
    async def info(self, ctx):
        e = discord.Embed(color=config.blue)
        
        channel_types = Counter(type(c) for c in self.bot.get_all_channels())
        voice = channel_types[discord.channel.VoiceChannel]
        text = channel_types[discord.channel.TextChannel]
        
        cpu_per = psutil.cpu_percent()
        cores = psutil.cpu_count()
        memory = psutil.virtual_memory().total >> 20
        mem_usage = psutil.virtual_memory().used >> 20
        storage_free = psutil.disk_usage('/').free >> 30
        
        e.description = f"""
__**Statistics**__
**Guilds:** {len(self.bot.guilds)}
**Users:** {len(self.bot.users)}
**Channels:**
- `{text:,}` text channels
-  `{voice:,}` voice channels

__**System**__
**Hosting OS:** `{platform.platform()}`
**Cores:** {cores}
**CPU:** {cpu_per}
**RAM:** {mem_usage}/{memory} MB
**Storage:** {storage_free} GB free
"""
        await ctx.send(embed=e)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            embed = discord.Embed(description=str(error), color=discord.Color.red())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(info(bot))
