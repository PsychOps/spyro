import discord, config
from discord.ext import commands

class sugg(commands.Cog, name="Suggestions"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx, *, args):
        try:
            self.bot.get_channel(817714676934377504)
            await ctx.message.delete()
            await ctx.send("test")
        except Exception as e:
            embed = discord.Embed(description=e, color=discord.Color.red())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(sugg(bot))
