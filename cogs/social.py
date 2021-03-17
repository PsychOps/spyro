import discord, config, random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class social(commands.Cog, name="Social"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(guild_ids=[820256957369679882], options = [{
                   "name": "user",
                   "description": "The person you want to hug!",
                   "type": 6,
                   "required": True
                   }])
    async def hug(self, ctx, user):
        """ Hug someone! """
        hug = ["https://media1.tenor.com/images/faf29ddc23059c5740751a3fecc2f303/tenor.gif?itemid=13533690",
               "https://media1.tenor.com/images/f20151a1f7e003426ca7f406b6f76c82/tenor.gif?itemid=13985247",
               "https://media1.tenor.com/images/8ac5ada8524d767b77d3d54239773e48/tenor.gif?itemid=16334628",
               "https://media1.tenor.com/images/68f16d787c2dfbf23a4783d4d048c78f/tenor.gif?itemid=9512793",
               "https://media1.tenor.com/images/3fee00811a33590e4ee490942f233c78/tenor.gif?itemid=14712845",
               "https://media1.tenor.com/images/2d13ede25b31d946284eaa3b8a4e6b31/tenor.gif?itemid=11990658",
               "https://media1.tenor.com/images/37df0fae36f9cce061c3cec84fc97a08/tenor.gif?itemid=17781844",
               "https://media1.tenor.com/images/ece75ca15b715aacd86724ee23604569/tenor.gif?itemid=16796068",
               "https://media2.giphy.com/media/gl8ymnpv4Sqha/giphy.gif"]
        embed = discord.Embed(description=f"{ctx.author.display_name} hugged {user.name} :sparkling_heart:", color=discord.Color.blue())
        embed.set_thumbnail(url=random.choice(hug))
        await ctx.respond()
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx: SlashContext, error):
        embed = discord.Embed(color=discord.Color.red())
        if ctx.author.id != 443217277580738571:
            embed.description = "You should probably report this bug to duck :p"
        embed.add_field(name='Full Traceback', value=f"```py\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}\n```", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(social(bot))
