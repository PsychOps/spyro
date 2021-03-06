import discord, config
from discord.ext import commands

class sugg(commands.Cog, name="Suggestions"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(817714676934377504)
        if message.channel != channel:
            return
        if message.author == self.bot.user:
            return
        if message.author == self.bot.fetch_user(620990340630970425):
            return
        await message.delete()
        e = discord.Embed(color=config.green)
        e.description = message.content
        e.set_author(name=message.author, icon_url=message.author.avatar_url)
        om = await channel.send(embed=e)
        await om.add_reaction('👍')
        await om.add_reaction('👎')
        await om.add_reaction('🤷')

def setup(bot):
    bot.add_cog(sugg(bot))
