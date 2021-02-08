import discord, config
from discord.ext import commands

class owner(commands.Cog, name="Owner"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief="unload a cog")
    @commands.is_owner()
    async def unload(self, ctx, *, cog):
        if cog == cogs.owner:
            await ctx.send('**You cannot unload the owner cog as this cog allows unloading/reloading/loading cogs.**')
            return
        try:
            self.bot.unload_extension(cog)
            await ctx.send(f'Successfully unloaded {cog}')
        except Exception as e:
            await ctx.send(f'Failed to unload {cog}\n```py\n{e}\n```')

def setup(bot):
    bot.add_cog(owner(bot))
