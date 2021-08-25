import discord, config, asyncio, datetime
import traceback
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

async def remove_reaction(payload):
    channel = payload.member.guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji, payload.member)

def staff():
    async def predicate(ctx):
        guild = ctx.bot.get_guild(834544478064607252)# Guild ID
        if ctx.guild is not None and ctx.guild == guild:
            member = guild.get_member(ctx.author.id)
            if member is not None:
                role = guild.get_role(862461768600125440)# Staff Role ID
                if role in member.roles:
                    return True
        return False
    return commands.check(predicate)

class custom(commands.Cog, name="Custom"):
    def __init__(self, bot):
        self.bot = bot
        self.suggestion_channel = 861577107528089630# Suggestion Channel
        self.guild = 834544478064607252# Guild ID
        self.channel = 862462066345902100# Staff Verification Channel ID
        self.message = 862463007476940820# Verification Message ID
        self.role = 862463200284639262# Awaiting Verification Role
        self.role2 = 861332359156465695# Member Role
        self.bot_role = 861561459015155722# Bot Role
        self.ping_channel = 861332244375535677# Verification Channel (for pings)
        self.general_chat = 861350638977024021# Main Chat (for welcome messages)

    @commands.Cog.listener('on_message')
    async def suggestions(self, message):
        if message.channel.id != self.suggestion_channel or message.author.id in [self.bot.user.id, 843252491473649665]:
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

    @commands.Cog.listener('on_raw_reaction_add')
    async def verification_reaction(self, payload):
        """ Checks for a Reaction on the Verification Message """
        if payload.message_id == self.message:
            role = payload.member.guild.get_role(self.role)
            role2 = payload.member.guild.get_role(self.role2)
            if role2 in payload.member.roles or payload.member.roles != [payload.member.guild.default_role]:
                return
            try:
                uembed = discord.Embed(title='Verification', description=f'Hey **{payload.member.display_name}**! Thanks for joining **{payload.member.guild.name}**.\nBefore joining our other members in chat, we\'ll need to verify you to make sure you\'re not a raider.\nPlease tell us why you want to be a part of the server and your sexuality. Thanks!', color=discord.Colour.blurple())
                uembed.set_author(name=payload.member.guild.name, icon_url=payload.member.guild.icon_url)
                uembed.set_footer(text='You have 5 minutes to respond.')
                msg = await payload.member.send(embed=uembed)
            except:
                return await remove_reaction(payload)
            else:
                def message_check(m):
                    if payload.member.id == m.author.id and payload.member.dm_channel.id == m.channel.id:
                        return True
                    return False
                try:
                    msg1 = await self.bot.wait_for('message', check=message_check, timeout=300.0)
                except asyncio.TimeoutError:
                    await msg.edit(content=f':x: You took too long to answer the question!')
                    return await remove_reaction(payload)
            channel = payload.member.guild.get_channel(self.channel)
            warning = ''
            if payload.member.created_at.replace(tzinfo=None) >= datetime.datetime.now() - datetime.timedelta(days=7):
                warning = f'\n:warning: This account was made {payload.member.created_at.strftime("%B %d %Y at %H:%M UTC")}'
            embed = discord.Embed(title='New Verification Request', description=f'{payload.member.mention} just requested verification!{warning}\n**Why do you want to join the server?**\n{msg1.content}', color=discord.Colour.blurple(), timestamp=payload.member.joined_at)
            embed.set_author(name=str(payload.member), icon_url=payload.member.avatar_url)
            embed.set_footer(text='This user joined the server')
            if msg1.attachments != []:
                embed.set_image(url=msg1.attachments[0].url)
            await channel.send(content=str(payload.member.id), embed=embed)# Sending the Verification Message
            await payload.member.send(f':white_check_mark: Submitted your Verification Request!\nYou will get a DM when it gets approved/denied.')
            await payload.member.add_roles(role, reason='Submitted Verification Request')

    @commands.group(invoke_without_command=True, aliases=['v'])
    async def verification(self, ctx):
        """ Verification Commands (Staff Only) """
        await ctx.send_help(ctx.command)

    @verification.command()
    @staff()
    async def approve(self, ctx, member: discord.Member):
        """ Approves a Verification Request """
        role = ctx.guild.get_role(self.role)
        role2 = ctx.guild.get_role(self.role2)
        if role not in member.roles:
            return await ctx.send(f':x: **{member.name}** does not have an Active Verification Request!')
        await member.remove_roles(role, reason=f'Verification Request Approved by {ctx.author} ({ctx.author.id})')
        await member.add_roles(role2, reason=f'Verification Request Approved by {ctx.author} ({ctx.author.id})')
        embed = discord.Embed(description=f'Your verification request for **{ctx.guild.name}** was approved __successfully__!\nYou can now retrieve your roles in <#861554760414003249> as well as chat with our fellow members in <#861350638977024021> :wave:', color=discord.Colour.blue())
        embed.set_author(name=str(member.guild.name), icon_url=str(member.guild.icon_url))
        msg = ''
        try:
            await member.send(embed=embed)
        except:
            msg = f'\n:warning: I am not able to DM {member.mention}!'
        await ctx.send(f':white_check_mark: Approved {member.name}\'s Verification Request!\n{msg}')
        general = ctx.guild.get_channel(self.general_chat)
        await general.send(f'<:pridemoji_ex1:861556592822059048> Welcome **{member.mention}** to the cabin! The safe haven for all LGBTQ members to meet. <:trans_kitty:861564763670315038>')

    @verification.command()
    @staff()
    async def deny(self, ctx, member: discord.Member):
        """ Deny a Verification Request """
        role = ctx.guild.get_role(self.role)
        if role not in member.roles:
            return await ctx.send(f':x: **{member.name}** does not have an Active Verification Request!')
        ban = '\U0001f528'
        kick = '\U0001f462'
        redo = '\U0001f501'
        cancel = '\U0000274c'
        msg = await ctx.send(f'Which of the following would you like to do when denying **{member.name}**?\n{ban} - Ban the User\n{kick} - Kick the User\n{redo} - Tell the User to Redo the Application\n{cancel} - Cancel this Menu')
        await msg.add_reaction(ban)
        await msg.add_reaction(kick)
        await msg.add_reaction(redo)
        await msg.add_reaction(cancel)
        def react_check(reaction, user):
            if ctx.author == user:
                if reaction.emoji in [ban, kick, redo, cancel]:
                    return True
            return False
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=react_check)
        except asyncio.TimeoutError:
            try:
                return await msg.clear_reactions()
            except:
                return await msg.edit(f':notepad_spiral: These options have timed out!')
        else:
            if reaction.emoji == cancel:
                try:
                    await msg.clear_reactions()
                except:
                    pass
                return await msg.edit(content=f':notepad_spiral: Canceled this request!')
            elif reaction.emoji == redo:
                embed = discord.Embed(description=f'Your Verification Request for **{ctx.guild.name}** has been denied!\nPlease redo your verification request by reacting to the message in <#{self.channel}>.', color=discord.Colour.red())
                embed.set_author(name=str(member.guild.name), icon_url=str(member.guild.icon_url))
                msg = ''
                try:
                    await member.send(embed=embed)
                except:
                    msg = f'\n:warning: I am not able to DM {member.mention}!'
                await member.remove_roles(role, reason=f'Redo Verification Request by {ctx.author} ({ctx.author.id})')
                await ctx.send(f':white_check_mark: Told **{member.name}** to redo their Verification Request!{msg}')
            elif reaction.emoji == kick:
                embed = discord.Embed(description=f'You\'ve been Kicked from **{ctx.guild.name}** for having an Invalid Verification Request.', color=discord.Colour.dark_orange())
                embed.set_author(name=str(member.guild.name), icon_url=str(member.guild.icon_url))
                msg = ''
                try:
                    await member.send(embed=embed)
                except:
                    msg = f'\n:warning: I am not able to DM {member.mention}!'
                await member.kick(reason=f'Denied Verification Request by {ctx.author} ({ctx.author.id})')
                await ctx.send(f':white_check_mark: Kicked {member.mention}!{msg}')
            elif reaction.emoji == ban:
                embed = discord.Embed(description=f'You\'ve been Banned from **{ctx.guild.name}** for having an Invalid Verification Request.', color=discord.Colour.dark_orange())
                embed.set_author(name=str(member.guild.name), icon_url=str(member.guild.icon_url))
                msg = ''
                try:
                    await member.send(embed=embed)
                except:
                    msg = f'\n:warning: I am not able to DM {member.mention}!'
                await member.ban(delete_message_days=7, reason=f'Denied Verification Request by {ctx.author} ({ctx.author.id})')
                await ctx.send(f':white_check_mark: Banned {member.mention}!{msg}')

def setup(bot):
    bot.add_cog(custom(bot))
