import discord, config, time, aiohttp, traceback, asyncio
import psutil, platform
from collections import Counter
from discord.ext import commands

class info(commands.Cog, name="Info"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def staff(self, ctx):
        the_list = []
        for user in ctx.guild.members:
            if ctx.channel.permissions_for(user).ban_members:
                the_list.append(str(user))
        e = discord.Embed(color=discord.Color.blue())
        e.description = ', '.join(the_list)
        await ctx.reply(embed=e)

    @commands.command()
    async def stafftest(self, ctx, *, permission):
        the_list = []
        for user in ctx.guild.members:
            test = permission
            if ctx.channel.permissions_for(user).(test):
                the_list.append(str(user))
        e = discord.Embed(color=discord.Color.blue())
        e.description = ', '.join(the_list)
        await ctx.reply(embed=e)
    
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
            msg = await ctx.send(embed=embed)
            if ctx.author.id in self.bot.owner_ids:
                await msg.add_reaction('\U0000203c')
                def react_check(reaction, user):
                    if ctx.author.id == user.id and reaction.emoji == '\U0000203c' and reaction.message.id == msg.id:
                        return True
                    return False
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=react_check)
                except asyncio.TimeoutError:
                    try:
                        await msg.remove_reaction('\U0000203c', self.bot.user)
                    except:
                        pass
                embed2 = discord.Embed(description=f"```py\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}\n```", color=discord.Color.red())
                await ctx.send(embed=embed2)
                try:
                    await msg.clear_reactions()
                except:
                    pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Tries to re-run a command when a message gets edited! """
        if after.author.bot is True or before.content == after.content:
            return
        prefixes = commands.when_mentioned_or('sp!')(self.bot, after)
        if after.content.startswith(tuple(prefixes)):
            ctx = await self.bot.get_context(after)
            msg = await self.bot.invoke(ctx)

def setup(bot):
    bot.add_cog(info(bot))
