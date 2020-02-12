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
from src.util import locales


class Help(commands.Cog):
    """Help commands"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC
        self._id = 162200556234866688

    def embed_exceptions(self, ctx, command, description: list=[]):
        prefix = read_prefix(ctx.guild.id)
        command = f"{prefix}{command}"
        embed = discord.Embed(
            title=command,
            color=self.colour,
            description='\n'.join(list((f"`{command} {x}`") for x in description)),
            timestamp=datetime.datetime.utcfromtimestamp(time.time())
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(
            text="Made with ❤️ by Taki#0853 (WIP)",
            icon_url=ctx.guild.me.avatar_url
        )
        return embed

    @commands.command()
    @trigger_typing
    async def ping(self, ctx):
        """Ping's Bot"""
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        before = time.monotonic()
        message = await ctx.send("🏓Ping!", delete_after=delay)
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(colour=0xff00,
                            title=lang_pack["command_ping_title"],
                            description="🏓Pong!\n{0} ms".format(int(ping)))
        embed.set_footer(
            text="Made with ❤️ by Taki#0853 (WIP)",
            icon_url=ctx.guild.me.avatar_url
        )
        try:
            await ctx.message.delete(delay=delay)
        except:
            pass
        await message.edit(content="", embed=embed)

    def embed_pagination(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        embed = discord.Embed(title=lang_pack["help_title"],
                            description=lang_pack["help_description"],
                            color=self.colour)
        embed.add_field(name='<:wf_market:641718306260385792> Warframe Market', value=lang_pack["help_waframe_market_description"])
        embed.add_field(name='<:ws:641721981292773376> Worldstate', value=lang_pack["help_worldstate_description"], inline=False)
        embed.add_field(name=u"\u2699 " + lang_pack["help_bot_utility_name"], value=lang_pack["help_bot_utility_value"])
        embed.add_field(
            name=lang_pack["help_donate"],
            value="[Kofi](https://ko-fi.com/takitsu)"
                  "\n[Patreon](https://www.patreon.com/takitsu)",
            inline=False
        )
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        return embed

    @commands.command()
    @commands.is_owner()
    async def emojis(self, ctx):
        emojis = await ctx.guild.fetch_emojis()
        await ctx.send(emojis)

    @staticmethod
    def _add_field(embed: object, command: dict):
        for k, v in command.items():
            embed.add_field(name=k, value=v, inline=False)

    @commands.command(aliases=["h"])
    @commands.bot_has_permissions(manage_messages=True, add_reactions=True)
    @trigger_typing
    async def help(self, ctx, arg=""):
        prefix = read_prefix(ctx.guild.id)
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        trade_command = {
            f"<{prefix}wtb | {prefix}b> <pc | xbox | ps4 | swi> [ITEM_NAME]" : lang_pack["help_wtb"],
            f"<{prefix}wts | {prefix}s> <pc | xbox | ps4 | swi> [ITEM_NAME]" : lang_pack["help_wts"],
            f"<{prefix}riven | {prefix}r> <pc | xbox | ps4 | swi> [ITEM_NAME]" : lang_pack["help_riven"],
            f"{prefix}ducats" : lang_pack["help_ducats"]
        }
        ws_command = {
            f"<{prefix}fissures | {prefix}f> <pc | ps4 | xb1 | swi> <FILTER>" : lang_pack["help_fissures"],
            f"{prefix}sortie" : lang_pack["help_sortie"],
            f"{prefix}baro" : lang_pack["help_baro"],
            f"{prefix}news <pc | xbox | ps4 | swi>" : lang_pack["help_news"],
            f"{prefix}earth" : lang_pack["help_earth"],
            f"{prefix}wiki [QUERY]" : lang_pack["help_wiki"],
            f"{prefix}event" : lang_pack["help_event"],
            f"{prefix}sentient": lang_pack["help_sentient"],
            f"{prefix}fish <cetus | fortuna>": lang_pack["help_fish"]
        }
        other_commands = {
            f"{prefix}bug [MESSAGE]" : lang_pack["help_bug"],
            f"{prefix}suggestion [MESSAGE]" : lang_pack["help_suggestion"],
            f"{prefix}ping" : lang_pack["help_ping"],
            f"{prefix}about" : lang_pack["help_about"],
            f"{prefix}donate" : lang_pack["help_donate"],
            f"{prefix}vote" : lang_pack["help_vote"],
            f"{prefix}support" : lang_pack["help_support"],
            f"{prefix}invite" : lang_pack["help_invite"],
            f"{prefix}language [COUNTRY_CODE]" : lang_pack["help_language"],
            f"{prefix}set_prefix [PREFIX]" : lang_pack["help_set_prefix"],
            f"{prefix}get_prefix" : lang_pack["help_get_prefix"],
            f"{prefix}settings [--delete] [n | no]" : lang_pack["help_settings_delete"],
            f"{prefix}settings [--delay] [TIME_IN_SECOND]" : lang_pack["help_settings_delay"],
            f"<{prefix}help | {prefix}h> <all>" : lang_pack["help_help"]
        }
        if not len(arg):
            toReact = ['⏪', '<:wf_market:641718306260385792>', '<:ws:641721981292773376>',u"\u2699"]
            embed = self.embed_pagination(ctx)
            pagination = await ctx.send(embed=embed)
            for reaction in toReact:
                await pagination.add_reaction(reaction)
            while True:

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in toReact
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=300.0)
                    emoji = str(reaction.emoji)
                except asyncio.TimeoutError:
                    try:
                        await ctx.message.delete()
                    except:
                        pass
                    return await pagination.delete()
                if '⏪' in emoji:
                    embed = self.embed_pagination(ctx)
                    thumb = ctx.guild.me.avatar_url
                elif '<:wf_market:641718306260385792>' in emoji:
                    embed = discord.Embed(title="<:wf_market:641718306260385792> Warframe Market",
                                        color=self.colour)
                    self._add_field(embed, trade_command)
                    thumb = "https://warframe.market/static/assets/frontend/logo_icon_only.png"

                elif '<:ws:641721981292773376>' in emoji:
                    embed = discord.Embed(title="<:ws:641721981292773376> Worldstate commands",
                                        color=self.colour)
                    self._add_field(embed, ws_command)
                    thumb = "https://avatars2.githubusercontent.com/u/24436369?s=280&v=4"
                elif u"\u2699" in emoji:
                    embed = discord.Embed(title=u"\u2699 Bot commands",
                                        color=self.colour)
                    self._add_field(embed, other_commands)
                    thumb = ctx.guild.me.avatar_url
                embed.set_thumbnail(url=thumb)
                embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                                icon_url=ctx.guild.me.avatar_url)
                await pagination.remove_reaction(reaction.emoji, user)
                await pagination.edit(embed=embed)
        elif arg == "all":
            commands = {
                "<:wf_market:641718306260385792> Warframe Market commands": trade_command,
                "<:ws:641721981292773376> Worldstate commands": ws_command,
                u"\u2699 Bot commands": other_commands
                }
            for k, v in commands.items():
                embed = discord.Embed(
                    title=k,
                    colour=self.colour,
                    description=lang_pack["help_description"]
                )
                self._add_field(embed, v)
                embed.set_thumbnail(url=ctx.guild.me.avatar_url)
                embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP)",
                    icon_url=ctx.guild.me.avatar_url
                    )
                await ctx.send(embed=embed)
        else:
            await ctx.send(message=lang_pack["command_help_invalide_arg"].format(ctx.author.mention, prefix))

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        self.bot._unload_extensions()
        self.bot._load_extensions()

    @help.error
    async def help_error(self, ctx, error):
        prefix = read_prefix(ctx.guild.id)
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        trade_command = f"""**`<{prefix}wtb | {prefix}b> <pc | xbox | ps4 | swi> [ITEM_NAME]`** - {lang_pack["help_wtb"]}
        **`<{prefix}wts | {prefix}s> <pc | xbox | ps4 | swi> [ITEM_NAME]`** - {lang_pack["help_wts"]}
        **`<{prefix}riven | {prefix}r> <pc | xbox | ps4 | swi> [ITEM_NAME]`** - {lang_pack["help_riven"]}
        **`{prefix}ducats`** - {lang_pack["help_ducats"]}"""
        ws_command = f"""**`<{prefix}fissures | {prefix}f> <pc | ps4 | xb1 | swi>`** - {lang_pack["help_fissures"]}
        **`{prefix}sortie`** - {lang_pack["help_sortie"]}
        **`{prefix}baro`** - {lang_pack["help_baro"]}
        **`{prefix}news <pc | xbox | ps4 | swi>`** - {lang_pack["help_news"]}
        **`{prefix}earth`** - {lang_pack["help_earth"]}
        **`{prefix}wiki [QUERY]`** - {lang_pack["help_wiki"]}
        **`{prefix}event`** - {lang_pack["help_event"]}
        **`{prefix}sentient`** - {lang_pack["help_sentient"]}
        **`{prefix}fish <cetus | fortuna>`** - {lang_pack["help_fish"]}"""
        other_commands = f"""**`{prefix}bug [MESSAGE]`** - {lang_pack["help_bug"]}
        **`{prefix}suggestion [MESSAGE]`** - {lang_pack["help_suggestion"]}
        **`{prefix}ping`** - {lang_pack["help_ping"]}
        **`{prefix}about`** - {lang_pack["help_about"]}
        **`{prefix}donate`** - {lang_pack["help_donate"]}
        **`{prefix}vote`** - {lang_pack["help_vote"]}
        **`{prefix}support`** - {lang_pack["help_support"],}
        **`{prefix}invite`** - {lang_pack["help_invite"]}
        **`{prefix}language [COUNTRY_CODE]`** - {lang_pack["help_language"]}
        **`{prefix}set_prefix [PREFIX]`** - {lang_pack["help_set_prefix"]}
        **`{prefix}get_prefix`** - {lang_pack["help_get_prefix"]}
        **`{prefix}settings [--delete] [n | no]`** - {lang_pack["help_settings_delete"]}
        **`{prefix}settings [--delay] [TIME_IN_SECOND]`** - {lang_pack["help_settings_delay"]}
        **`<{prefix}help | {prefix}h> <all>`** - {lang_pack["help_help"]}"""
        embed = discord.Embed(title=lang_pack["help_error"],
                            colour=self.colour,
                            description=lang_pack["help_description"])
        embed.add_field(name="Warframe Market commands", value=trade_command, inline=False)
        embed.add_field(name="Worldstate commands", value=ws_command, inline=False)
        embed.add_field(name="Bot commands", value=other_commands, inline=False)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        await ctx.author.send(embed=embed)

    @commands.command()
    @trigger_typing
    async def language(self, ctx, lang=""):
        to_delete, delay, old = read_settings(ctx.guild.id)
        if len(lang):
            if lang in ("fr", "en", "de", "es", "it", "ja","ko", "pl", "pt", "ru", "tc", "tr", "zh"):
                update_lang_server(ctx.guild.id, lang)
                lang_pack = locales(lang)
                embed = discord.Embed(
                    title=lang_pack["command_language_title"],
                    description=lang_pack["command_language_description"].format(old, ctx.guild.id, lang),
                    colour=self.colour
                )
            else:
                lang_pack = locales(old)
                embed = discord.Embed(
                    title=lang_pack["command_language_title"],
                    description=lang_pack["command_language_description_error"].format(lang),
                    colour=self.colour
                )
        else:
            lang_pack = locales(old)
            embed = discord.Embed(
                title=lang_pack["command_language_title"],
                description=lang_pack["command_language_description_no_lang"].format(old, ctx.guild.id),
                colour=self.colour
            )
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def invite(self,ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        embed = discord.Embed(
                        title=lang_pack["invite_bot"],
                        description=f'[{lang_pack["click_here"]}](https://discordapp.com/oauth2/authorize?client_id=593364281572196353&scope=bot&permissions=470083648)',
                        colour=self.colour
                    )
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                         icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(pass_context=True)
    @trigger_typing
    async def vote(self,ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        embed = discord.Embed(title=lang_pack["command_vote_title"],
                              description=f'[{lang_pack["click_here"]}](https://top.gg/bot/593364281572196353/vote)',
                              colour=self.colour)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(pass_context=True)
    @trigger_typing
    async def support(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        embed = discord.Embed(title=lang_pack["discord_support_title"],
                               description=f'[{lang_pack["click_here"]}](https://discordapp.com/invite/wTxbQYb)',
                                colour=self.colour)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(pass_context=True)
    @trigger_typing
    async def donate(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        embed = discord.Embed(title=lang_pack["donate"],
                              colour=self.colour)
        embed.add_field(name="Patreon", value=f'[{lang_pack["click_here"]}](https://www.patreon.com/takitsu)')
        embed.add_field(name=lang_pack["kofi"], value=f"[{lang_pack['click_here']}](https://ko-fi.com/takitsu)")
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(pass_context=True)
    @trigger_typing
    async def about(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        prefix = read_prefix(ctx.guild.id)
        embed = discord.Embed(
                            timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                            color=self.colour
                        )
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.add_field(name=lang_pack["invite_bot"],
                        value=f"[{lang_pack['click_here']}](https://discordapp.com/oauth2/authorize?client_id=593364281572196353&scope=bot&permissions=470083648)",
                        inline=False)
        embed.add_field(name=lang_pack["discord_support_title"],
                        value=f"[{lang_pack['click_here']}](https://discordapp.com/invite/wTxbQYb)",
                        inline=False)
        embed.add_field(name=lang_pack["donate"],
                        value="[Patreon](https://www.patreon.com/takitsu)\n[Kofi](https://ko-fi.com/takitsu)",
                        inline=False)
        embed.add_field(name=lang_pack["command_about_title"],
                        value=f"{prefix}help")
        nb_users = 0
        for s in self.bot.guilds:
            nb_users += len(s.members)

        embed.add_field(name=lang_pack["servers"], value=len(self.bot.guilds))
        embed.add_field(name=lang_pack["members"], value=nb_users)
        embed.add_field(name=lang_pack["creator"], value="Taki#0853")
        embed.add_field(name=lang_pack["igname"], value="Takitsu21")
        embed.add_field(
            name=lang_pack["command_about_contributor"],
            value="Ralagane, Taki : fr",
            inline=False
        )
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx, *args):
        arg_l = len(args)
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        if not arg_l:
            embed = discord.Embed(
                title=lang_pack["command_settings_update"],
                description=lang_pack["command_settings_check_description"].format(ctx.guild.id),
                timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                color=self.colour
            )
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name=lang_pack["command_settings_delete_title"], value=lang_pack[convert_str(to_delete)])
            embed.add_field(name=lang_pack["command_settings_delay"], value=delay)
            embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        elif arg_l == 2 and args[0] == '--delay':
            try:
                delay = abs(int(args[1]))
                u_guild_settings(ctx.guild.id, 1, delay)
                embed = discord.Embed(
                    title=lang_pack["command_settings_update"],
                    description=lang_pack["command_settings_check_description_updated"].format(ctx.guild.id),
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    color=self.colour
                )
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.add_field(name=lang_pack["command_settings_delete_title"], value=lang_pack["yes"])
                embed.add_field(name=lang_pack["command_settings_delay"], value=delay)
                embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
                return await e_send(ctx, 1, embed=embed, delay=delay)
            except:
                to_delete, delay, lang = read_settings(ctx.guild.id)
                embed = self.embed_exceptions(ctx, "settings", description=["[--delay] [TIME_IN_SECOND]"])
                await e_send(ctx, to_delete, embed=embed, delay=delay)
        elif arg_l == 2 and args[0] == '--delete':
            try:
                delete = convert_str(args[1])
                delete_bool = convert_bool(args[1])
                u_guild_settings(ctx.guild.id, delete_bool, None)
                embed = discord.Embed(
                    title=lang_pack["command_settings_update"],
                    description=lang_pack["command_settings_check_description_updated"].format(ctx.guild.id),
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    color=self.colour
                )
                embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.add_field(name=lang_pack["command_settings_delete_title"], value=delete)
                to_delete, delay, lang = read_settings(ctx.guild.id)
                return await e_send(ctx, to_delete, embed=embed, delay=delay)
            except:
                to_delete, delay, lang = read_settings(ctx.guild.id)
                embed = self.embed_exceptions(ctx, "settings", description=["[--delete] [y | n]"])
                await e_send(ctx, to_delete, embed=embed, delay=delay)
        else:
            to_delete, delay, lang = read_settings(ctx.guild.id)
            embed = self.embed_exceptions(ctx, "settings", description=["[--delete] [y | n]", "[--delay] [TIME_IN_SECOND]"])
            await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, *, prefixes=""):
        u_prefix(ctx.guild.id, prefixes)
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        await ctx.send(lang_pack["command_set_prefix"].format(prefixes))

    @commands.command()
    @commands.is_owner()
    async def init_db(self, ctx):
        for s in self.bot.guilds:
            try:
                i_guild_settings(s.id, '*', 0, None)
            except:
                pass

    @commands.command()
    @trigger_typing
    async def get_prefix(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        embed = discord.Embed(
            title=lang_pack["command_get_prefix_title"],
            description=read_prefix(ctx.guild.id),
            timestamp=datetime.datetime.utcfromtimestamp(time.time()),
            color=self.colour
        )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def suggestion(self, ctx, *message):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        if len(message) < 3:
            embed = discord.Embed(title=lang_pack["command_suggestion_title"],
                                colour=self.colour,
                                description=lang_pack["message_too_short"].format(ctx.author.mention),
                                icon_url=ctx.guild.me.avatar_url)
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                            icon_url=ctx.guild.me.avatar_url)
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        dm = self.bot.get_user(self._id)
        message = ' '.join(message)
        await dm.send(f"[{ctx.author} - SUGGEST] -> {message}")
        embed = discord.Embed(title=lang_pack["command_suggestion_title"],
                            colour=self.colour,
                            description=lang_pack["command_suggestion_sent"].format(ctx.author.mention),
                            icon_url=ctx.guild.me.avatar_url)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        return await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def bug(self, ctx, *message):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        if len(message) < 3:
            embed = discord.Embed(title=lang_pack["command_bug_title"],
                    colour=self.colour,
                    description=lang_pack["message_too_short"].format(ctx.author.mention),
                    icon_url=ctx.guild.me.avatar_url)
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                            icon_url=ctx.guild.me.avatar_url)
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        dm = self.bot.get_user(self._id)
        message = ' '.join(message)
        await dm.send(f"[{ctx.author} - BUG] -> {message}")
        embed = discord.Embed(title=lang_pack["command_bug_title"],
                            colour=self.colour,
                            description=lang_pack["command_bug_sent"].format(ctx.author.mention),
                            icon_url=ctx.guild.me.avatar_url)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        return await e_send(ctx, to_delete, embed=embed, delay=delay)

def setup(bot):
    bot.add_cog(Help(bot))
