#!/usr/bin/env python3
# coding:utf-8

import discord
import time
from discord.ext import commands
from src.decorators import trigger_typing
import asyncio
from src._discord import *
import datetime
from src.sql import *


class Help(commands.Cog):
    """Help commands"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC
        self._id = 162200556234866688

    @commands.command()
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def ping(self, ctx):
        """Ping's Bot"""
        to_delete, delay = read_settings(ctx.guild.id)
        before = time.monotonic()
        message = await ctx.send("🏓Pong!", delete_after=delay)
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(colour=0xff00,
                            title="Warframe Trader ping",
                            description=f"🏓{int(ping)} ms")
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(
            text="Made with ❤️ by Taki#0853 (WIP)",
            icon_url=ctx.guild.me.avatar_url
        )
        await ctx.message.delete(delay=delay)
        await message.edit(content="", embed=embed)

    def embed_pagination(self, ctx):
        embed = discord.Embed(title="Help hub",
                            description="[Vote here](https://top.gg/bot/551446491886125059) to support me if you ❤️ the bot\n"
                            "`[RequiredArgument] <Parameter | To | Choose>`",
                            color=self.colour)
        embed.add_field(name='<:wf_market:641718306260385792> Warframe Market', value="View commands about warframe.market(WTS, WTB, stats).")
        embed.add_field(name='<:ws:641721981292773376> Worldstate', value="View commands about arbitration, sortie, baro etc...", inline=False)
        embed.add_field(name=u"\u2699 Warframe Trader utility", value="View commands about the bot")
        embed.add_field(
            name="If you want to support me",
            value="[Kofi](https://ko-fi.com/takitsu)"
                  "\n[Patreon](https://www.patreon.com/takitsu)"
        )
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        return embed 

    @commands.command()
    @commands.is_owner()
    async def emojis(self, ctx):
        emojis = await ctx.guild.fetch_emojis()
        await ctx.send(emojis)
        await ctx.send("<:_red_circle:643936812527779850>, <:_green_circle:643936852327530548>, <:_purple_circle:643936797222764554> ")

    @commands.command(aliases=["h"])
    @commands.bot_has_permissions(manage_messages=True, add_reactions=True)
    @trigger_typing
    async def help(self, ctx):
        prefix = read_prefix(ctx.guild.id)
        trade_command = f"""**`<{prefix}wtb | {prefix}b> <pc | xbox | ps4 | swi> [ITEM_NAME]`** - View 7 sellers sort by prices and status (Online in game)\n
        **`<{prefix}wts | {prefix}s> <pc | xbox | ps4 | swi> [ITEM_NAME]`** - View 7 buyers sort by prices and status (Online in game)\n
        **`<{prefix}riven | {prefix}r> <pc | xbox | ps4 | swi> [ITEM_NAME]`** - Views 6 riven mod sorted by ascending prices and status (Online in game)\n
        **`{prefix}ducats`** - View 12 worth it items to sell in ducats"""
        ws_command = f"""**`<{prefix}fissures | {prefix}f> <pc | ps4 | xb1 | swi>`** - View current fissures available\n
        **`{prefix}sortie`** - View current sortie\n
        **`{prefix}baro`** - View baro ki'teer inventory and dates\n
        **`<{prefix}news <pc | xbox | ps4 | swi>`** - View news about Warframe\n
        **`{prefix}earth`** - View earth cycle"""
        other_commands = f"""**`{prefix}bug [MESSAGE]`** - Send me a bug report, this will helps to improve the bot\n
        **`{prefix}suggestion [MESSAGE]`** - Suggestion to add for the bot, all suggestions are good don't hesitate\n
        **`{prefix}ping`** - View bot latency\n
        **`{prefix}about`** - Bot info\n
        **`{prefix}donate`** - Link to support me\n
        **`{prefix}vote`** - An other way to support me\n
        **`{prefix}support`** - Discord support if you need help or want to discuss with me\n
        **`{prefix}invite`** - View bot link invite\n
        **`{prefix}set_prefix [PREFIX]`** - Set new prefix\n
        **`{prefix}get_prefix`** - View actual guild prefix\n
        **`<{prefix}help | {prefix}h>`** - View bot commands"""

        toReact = ['⏪', '<:wf_market:641718306260385792>', '<:ws:641721981292773376>',u"\u2699"]
        embed = self.embed_pagination(ctx)
        pagination = await ctx.send(embed=embed)
        while True:
            for reaction in toReact:
                await pagination.add_reaction(reaction)
            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in toReact
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                await ctx.message.delete()
                return await pagination.delete()
            if '⏪' in str(reaction.emoji):
                embed = self.embed_pagination(ctx)
            elif '<:wf_market:641718306260385792>' in str(reaction.emoji):
                embed = discord.Embed(title="<:wf_market:641718306260385792> Market",
                                    description=trade_command,
                                    color=self.colour)
            elif '<:ws:641721981292773376>' in str(reaction.emoji):
                embed = discord.Embed(title="<:ws:641721981292773376> Worldstate",
                                    description=ws_command,
                                    color=self.colour)

                
                await pagination.edit(embed=embed)
            elif u"\u2699" in str(reaction.emoji):
                embed = discord.Embed(title=u"\u2699 Bot",
                                    description=other_commands,
                                    color=self.colour)
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                            icon_url=ctx.guild.me.avatar_url)
            await pagination.edit(embed=embed)

    @commands.command(pass_context=True)
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def invite(self,ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        embed = discord.Embed(
                        title='Invite me',
                        description='[Click here](https://discordapp.com/oauth2/authorize?client_id=593364281572196353&scope=bot&permissions=470083648)',
                        colour=self.colour
                    )
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(pass_context=True)
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def vote(self,ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        embed = discord.Embed(title='Vote for Warframe Trader',
                              description='[Click here](https://discordbots.org/bot/551446491886125059/vote)',
                              colour=self.colour)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(pass_context=True)
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def support(self,ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        embed = discord.Embed(title='Discord support',
                               description='[Click here](https://discordapp.com/invite/wTxbQYb)',
                                colour=self.colour)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(pass_context=True)
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def donate(self, ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        embed = discord.Embed(title='Donate',
                              colour=self.colour)
        embed.add_field(name="Patreon", value='[Click here](https://www.patreon.com/takitsu)')
        embed.add_field(name="Buy me a Kofi", value="[Click here](https://ko-fi.com/takitsu)")
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(pass_context=True)
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def about(self, ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        prefix = read_prefix(ctx.guild.id)
        embed = discord.Embed(
                            timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                            color=self.colour
                        )
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.add_field(name="Invite Warframe Trader",
                        value="[Click here](https://discordapp.com/oauth2/authorize?client_id=593364281572196353&scope=bot&permissions=470083648)")
        embed.add_field(name="Discord Support",
                        value="[Click here](https://discordapp.com/invite/wTxbQYb)")
        embed.add_field(name="Donate",value="[Patreon](https://www.patreon.com/takitsu)\n[Kofi](https://ko-fi.com/takitsu)")
        embed.add_field(name="Help command",value=f"{prefix}help")
        nb_users = 0
        for s in self.bot.guilds:
            nb_users += len(s.members)

        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Members", value=nb_users)
        embed.add_field(name="**Creator**", value="Taki#0853")
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx, *args):
        arg_l = len(args)
        if not arg_l:
            to_delete, delay = read_settings(ctx.guild.id)
            embed = discord.Embed(
                title="Settings",
                description=f"Here is your guild settings ({ctx.guild.id})",
                timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                color=self.colour
            )
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name="Delete messages", value=convert_str(to_delete))
            embed.add_field(name="Delay", value=delay)
            embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        elif arg_l == 2 and args[0] == '--delay':
            try:
                delay = abs(int(args[1]))
                u_guild_settings(ctx.guild.id, 1, delay)
                embed = discord.Embed(
                    title="Settings Updated",
                    description=f"Your guild settings ({ctx.guild.id}) has been updated",
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    color=self.colour
                )
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.add_field(name="Delete messages", value='Yes')
                embed.add_field(name="Delay", value=delay)
                embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
                return await e_send(ctx, 1, embed=embed, delay=delay)
            except (TypeError, ValueError):
                await ctx.send("Syntax error\nRetry with `*settings --delay [TIME_IN_SECOND]`")
        elif arg_l == 2 and args[0] == '--delete':
            try:
                delete = convert_str(args[1])
                delete_bool = convert_bool(args[1])
                u_guild_settings(ctx.guild.id, delete_bool, None)
                embed = discord.Embed(
                    title="Settings Updated",
                    description=f"Your guild settings ({ctx.guild.id}) has been updated",
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    color=self.colour
                )
                embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.add_field(name="Delete messages", value=delete)
                to_delete, delay = read_settings(ctx.guild.id)
                return await e_send(ctx, to_delete, embed=embed, delay=delay)
            except TypeError:
                await ctx.send("Syntax error\nRetry with `*settings --delete [y | n]`")
        else:
            to_delete, delay = read_settings(ctx.guild.id)
            prefix = read_prefix(ctx.guild.id)
            embed = discord.Embed(
                    title=f"{prefix}settings",
                    description=f"`{prefix}settings [--delete] [y | n]`\n"
                                f"`{prefix}settings [--delay] [TIME_IN_SECOND]`",
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    color=self.colour
                )
            embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                    icon_url=ctx.guild.me.avatar_url)
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, *, prefixes=""):
        u_prefix(ctx.guild.id, prefixes)
        await ctx.send(f"New prefix set : `{prefixes}`")

    @commands.command()
    @commands.is_owner()
    async def init_db(self, ctx):
        for s in self.bot.guilds:
            try:
                i_guild_settings(s.id, '*', 0, None)
            except:
                pass

    @trigger_typing
    @commands.command()
    async def get_prefix(self, ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        embed = discord.Embed(
            title="Prefix",
            description=read_prefix(ctx.guild.id),
            timestamp=datetime.datetime.utcfromtimestamp(time.time()),
            color=self.colour
        )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @trigger_typing
    @commands.command()
    async def suggestion(self, ctx, *message):
        to_delete, delay = read_settings(ctx.guild.id)
        await ctx.message.delete(delay=delay)
        if not len(message) or len(message) < 3:
            embed = discord.Embed(title='**Suggestion**',
                                colour=self.colour,
                                description=f"{ctx.author.mention} Message too short!\nAt least 3 words required",
                                icon_url=ctx.guild.me.avatar_url)
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                            icon_url=ctx.guild.me.avatar_url)
            return await ctx.send(embed=embed, delete_after=delay)
        dm = self.bot.get_user(self._id)
        message = ' '.join(message)
        await dm.send(f"[{ctx.author} - SUGGEST] -> {message}")
        embed = discord.Embed(title='**Suggestion**',
                            colour=self.colour,
                            description=f"{ctx.author.mention} Your suggestion has been sent @Taki#0853\nThanks for the feedback",
                            icon_url=ctx.guild.me.avatar_url)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        return await ctx.send(embed=embed, delete_after=delay)

    @trigger_typing
    @commands.command()
    async def bug(self, ctx, *message):
        to_delete, delay = read_settings(ctx.guild.id)
        await ctx.message.delete(delay=delay)
        if not len(message) or len(message) < 3:
            embed = discord.Embed(title='**Bug Report**',
                    colour=self.colour,
                    description=f"{ctx.author.mention} Message too short!\nAt least 3 words required",
                    icon_url=ctx.guild.me.avatar_url)
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                            icon_url=ctx.guild.me.avatar_url)
            return await ctx.send(embed=embed, delete_after=delay)
        dm = self.bot.get_user(self._id)
        message = ' '.join(message)
        await dm.send(f"[{ctx.author} - BUG] -> {message}")
        embed = discord.Embed(title='**Bug Report**',
                            colour=self.colour,
                            description=f"{ctx.author.mention} Your bug report has been sent @Taki#0853\nThanks for the feedback",
                            icon_url=ctx.guild.me.avatar_url)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        return await ctx.send(embed=embed, delete_after=delay)

def setup(bot):
    bot.add_cog(Help(bot))
