#!/usr/bin/env python3
# coding:utf-8

import discord
import time
from discord.ext import commands
from src.decorators import trigger_typing
import asyncio


class Help(commands.Cog):
    """Help commands"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC

    @commands.command()
    @trigger_typing
    async def ping(self,ctx):
        """Ping's Bot"""
        before = time.monotonic()
        message = await ctx.send("🏓Pong!")
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(colour=0xff00,
                            title="Warframe Trader ping",
                            description=f"🏓{int(ping)} ms")
        embed.set_thumbnail(url=ctx.guild.me.avatar.url)
        embed.set_footer(
            text="Made with ❤️ by Taki#0853 (WIP)",
            icon_url=ctx.guild.me.avatar_url
        )
        await message.edit(content="", embed=embed)

    def embed_pagination(self, ctx):
        embed = discord.Embed(title="Help hub",
                            description="[Vote here](https://top.gg/bot/551446491886125059) to support me if you ❤️ the bot\n"
                            "`[RequiredArgument] <ParameterToChoose>`",
                            color=self.colour)
        embed.add_field(name='<:wf_market:641718306260385792> Warframe Market', value="View commands about warframe.market(WTS, WTB, stats).")
        embed.add_field(name='<:ws:641721981292773376> Worldstate', value="View commands about arbitration, sortie, baro etc...")
        embed.add_field(name=u"\u2699 About Warframe Trader", value="View commands about the bot")
        embed.add_field(
            name="If you want to support me",
            value="[Kofi](https://ko-fi.com/takitsu)"
                  "\n[Patreon](https://www.patreon.com/takitsu)"
        )
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        return embed 

    @commands.command()
    async def emojis(self, ctx):
        emojis = await ctx.guild.fetch_emojis()
        await ctx.send(emojis)
        await ctx.send("<:wf_market:641718306260385792>")

    @commands.command(aliases=["h"])
    @commands.bot_has_permissions(manage_messages=True, add_reactions=True)
    @trigger_typing
    async def help(self, ctx):
        await ctx.message.delete()
        trade_command = """**`<a!stats | a!s>`** - Explanation about stats\n
        **`<a!stats | a!s> [USERNAME] <pc | xbox | psn>`** - View Apex Legends statistics -> Example `a!s nicehat_taki pc`\n
        **`<a!stats | a!s> [USERNAME]`** - View Apex Legends statistics for PC only (shortcut) -> Example `a!s nicehat_taki\n
        **`<a!profile | a!p>`** - View your Apex Legends profile if registered before\n
        **`<a!profile | a!p> save [USERNAME] <pc | xbox | psn>`** - Link your Discord account to your Apex Legends stats -> Example `a!p save nicehat_taki pc`\n
        **`<a!profile | a!p> display`** - View the current saved profile\n
        **`<a!profile | a!p> unlink`** - Unlink your profile\n
        **`a!history [USERNAME] <pc | xbox | psn>`** - View player's recent matches"""
        ws_command = """**`<*fissures | *f> <pc | ps4 | xb1 | swi>`** - View current fissures available\n
        **`*sortie`** - View current sortie\n
        **`a!legend`** - Random legend to pick for the next game\n
        **`a!team`** - Entire random team for the next game\n
        **`a!weapons`** - List all weapon commands to get their informations"""
        other_commands = """**`*bug [MESSAGE]`** - Send me a bug report, this will helps to improve the bot\n
        **`*suggestion [MESSAGE]`** - Suggestion to add for the bot, all suggestions are good don't hesitate\n
        **`*ping`** - View bot latency\n
        **`*about`** - Bot info\n
        **`*donate`** - Link to support me\n
        **`*vote`** - An other way to support me\n
        **`*support`** - Discord support if you need help or want to discuss with me\n
        **`*invite`** - View bot link invite\n
        **`<*help | *h>`** - View bot commands"""

        toReact = ['⏪', '<:wf_market:641718306260385792>', '<:ws:641721981292773376>',u"\u2699"]
        # emojis = await ctx.guild.fetch_emojis()
        embed = self.embed_pagination(ctx)
        pagination = await ctx.send(embed=embed)
        while True:
            for reaction in toReact:
                await pagination.add_reaction(reaction)
            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in toReact
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=180.0)
            except asyncio.TimeoutError:
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
            elif '<:ws:641721981292773376>' in str(reaction.emoji):
                embed = discord.Embed(title="📃 News",
                                    description=news_command,
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


def setup(bot):
    bot.add_cog(Help(bot))
