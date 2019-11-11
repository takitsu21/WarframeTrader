#!/usr/bin/env python3
# coding:utf-8

import discord
import time
from discord.ext import commands
from src.decorators import trigger_typing
import asyncio
from src._discord import e_send
import datetime


class Help(commands.Cog):
    """Help commands"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC

    @commands.command()
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def ping(self, ctx):
        """Ping's Bot"""
        await ctx.message.delete()
        before = time.monotonic()
        message = await ctx.send("🏓Pong!", delete_after=30)
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(colour=0xff00,
                            title="Warframe Trader ping",
                            description=f"🏓{int(ping)} ms")
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
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
        embed.add_field(name='<:ws:641721981292773376> Worldstat', value="View commands about arbitration, sortie, baro etc...")
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
        trade_command = """**`<*wtb | *b> <pc | xbox | ps4 | swi> [ITEM_NAME]`** - View 7 sellers sort by prices and status (Online in game)\n
        **`<*wts | *s> <pc | xbox | ps4 | swi> [ITEM_NAME]`** - View 7 buyers sort by prices and status (Online in game)\n
        **`<*wtb | *b> <pc | xbox | ps4 | swi> [ITEM_NAME]`** - View 7 sellers sort by prices and status (Online in game)\n
        **`*ducats`** - View 12 worth it items to sell in ducats\n"""
        ws_command = """**`<*fissures | *f> <pc | ps4 | xb1 | swi>`** - View current fissures available\n
        **`*sortie`** - View current sortie\n
        **`*baro`** - View baro ki'teer inventory and dates\n
        **`*news`** - View news about Warframe\n"""
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
                embed = discord.Embed(title="<:ws:641721981292773376> Worldstat",
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
        embed = discord.Embed(
                        title='**Invite me** :',
                        description='[**here**](https://discordapp.com/oauth2/authorize?client_id=551446491886125059&scope=bot&permissions=8)',
                        colour=self.colour
                    )
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, embed=embed, delay=300)

    @commands.command(pass_context=True)
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def vote(self,ctx):
        embed = discord.Embed(title='**Vote for Warframe Trader**',
                              description='[**Click here**](https://discordbots.org/bot/551446491886125059/vote)',
                              colour=self.colour)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, embed=embed, delay=300)

    @commands.command(pass_context=True)
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def support(self,ctx):
        embed = discord.Embed(title='Discord support',
                               description='[Taki Support Server](https://discordapp.com/invite/wTxbQYb)',
                                colour=self.colour)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, embed=embed, delay=300)

    @commands.command(pass_context=True)
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def donate(self, ctx):
        embed = discord.Embed(title='Donate',
                              colour=self.colour)
        embed.add_field(name="Patreon", value='[Click here](https://www.patreon.com/takitsu)')
        embed.add_field(name="Buy me a Kofi", value="[Click here](https://ko-fi.com/takitsu)")
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, embed=embed, delay=300)

    @commands.command(pass_context=True)
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def about(self, ctx):
        embed = discord.Embed(
                            timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                            color=self.colour
                        )
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.add_field(name="Vote",
                        value="[Click here](https://discordbots.org/bot/551446491886125059/vote)")
        embed.add_field(name="Invite Warframe Trader",
                        value="[Click here](https://discordapp.com/oauth2/authorize?client_id=551446491886125059&scope=bot&permissions=1543825472)")
        embed.add_field(name="Discord Support",
                        value="[Click here](https://discordapp.com/invite/wTxbQYb)")
        embed.add_field(name="Donate",value="[Patreon](https://www.patreon.com/takitsu)\n[Kofi](https://ko-fi.com/takitsu)")
        embed.add_field(name="Help command",value="*help")
        nb_users = 0
        for s in self.bot.guilds:
            nb_users += len(s.members)

        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Members", value=nb_users)
        embed.add_field(name="**Creator**", value="Taki#0853")
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, embed=embed, delay=300)



def setup(bot):
    bot.add_cog(Help(bot))
