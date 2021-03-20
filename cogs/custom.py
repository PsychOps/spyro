import discord, config, asyncio, datetime
import traceback
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class custom(commands.Cog, name="Custom"):
    def __init__(self, bot):
        self.bot = bot
        self.suggestion_channel = 820259145830760449# Suggestion Channel

    @commands.Cog.listener('on_message')
    async def suggestions(self, message):
        if message.channel.id != self.suggestion_channel or message.author.id in [self.bot.user.id, 620990340630970425]:
            return
        elif message.author.bot is True:
            return await message.delete()
        elif message.content.startswith('! ') and message.author.guild_permissions.administrator is True:
            if message.reference is not None:
                msg = await message.channel.fetch_message(message.reference.message_id)
                embed = msg.embeds[0]
                embed.add_field(name=f'Comment from {message.author.name}', value=str(message.content)[2:])
                await msg.edit(embed=embed)
                await message.delete()
            return
        await message.delete()
        channel = self.bot.get_channel(self.suggestion_channel)
        embed = discord.Embed(description=str(message.content), color=config.green)
        embed.set_author(name=str(message.author), icon_url=str(message.author.avatar_url))
        if message.attachments != []:
            embed.set_image(url=message.attachments[0].url)
        embed2 = await channel.send(embed=embed)
        await embed2.add_reaction('👍')
        await embed2.add_reaction('🤷')
        await embed2.add_reaction('👎')

    @commands.Cog.listener()
    async def on_member_join(member):
            channel = self.bot.get_channel(715969701771083820)
            await member.send("<@&822886791312703518> be sure to welcome our new member!")
        
        
def setup(bot):
    bot.add_cog(custom(bot))
