import discord, config
from discord.ext import commands

class owner(commands.Cog, name="Owner"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief="unload a cog")
    @commands.is_owner()
    async def unload(self, ctx, *, cog):
        if cog == 'cogs.owner':
            await ctx.send('**You cannot unload the owner cog as this cog allows unloading/reloading/loading cogs.**')
            return
        #if cog == '~':
        #    self.bot.unload_extension(config.extensions)
        #    await ctx.send(f'Successfully unloaded {config.extensions}
        try:
            self.bot.unload_extension(cog)
            await ctx.send(f'Successfully unloaded`{cog}`.')
        except Exception as e:
            await ctx.send(f'Failed to unload {cog}\n```py\n{e}\n```')
            
    @commands.command(brief="load a cog")
    @commands.is_owner()
    async def load(self, ctx, *, cog):
        try:
            self.bot.load_extension(cog)
            await ctx.send(f'Successfully loaded `{cog}`.')
        except Exception as e:
            await ctx.send(f'Failed to load {cog}\n```py\n{e}\n```')
            
    @commands.command(brief="Reload a cog")
    @commands.is_owner()
    async def reload(self, ctx, *, cog):
        if cog == '~':
            try:
                self.bot.reload_extension(config.extensions)
                await ctx.send(f'Successfully reloaded {config.extensions}')
            except Exception as e:
                await ctx.send(f'Failed to load {config.extensions}\n```py\n{e}\n```')
        else:
            try:
                self.bot.reload_extension(cog)
                await ctx.send(f'Successfully reloaded `{cog}`.')
            except Exception as e:
                await ctx.send(f'Failed to load {cog}\n```py\n{e}\n```')

    @commands.command(name="shutdown", aliases=["logout"])
    @commands.is_owner()
    async def jsk_shutdown(self, ctx: commands.Context):
        """
        Logs this bot out.
        """

        await ctx.send("Logging out now")
        await self.bot.logout()

def setup(bot):
    bot.add_cog(owner(bot))
