import discord, config
from discord.ext import commands

class owner(commands.Cog, name="Owner"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief="unload a cog")
    @commands.is_owner()
    async def unload(self, ctx, *, cogg):
        try:
            cog = self.bot.get_cog(cogg)
            self.bot.unload_extension(cog)
            await ctx.send(f'Successfully unloaded {cog}')
        except:
            await ctx.send(f'Failed to unload {cog}')
    

def setup(bot):
    bot.add_cog(owner(bot))
