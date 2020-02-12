#!/usr/bin/env python3
# coding:utf-8
import discord
import time
import datetime
from discord.ext import commands
from src.worldstate import *
from src._discord import *
from src.decorators import trigger_typing
from src.sql import *
import logging
from src.util import locales


logger = logging.getLogger('warframe')


class WorldState(commands.Cog):
    """Warframe worldstate data"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC
        self.footer_ws = "Made with ❤️ by Taki#0853 (WIP) | using api.warframestat.us"
        self.thumb_dev_comm = 'https://avatars2.githubusercontent.com/u/24436369?s=280&v=4'

    @commands.command(aliases=["f"])
    @trigger_typing
    async def fissures(self, ctx, platform: str=None, *highlight):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        if platform is not None and platform.lower() in ["pc", "xb1", "ps4", "swi"]:
            if len(highlight):
                highlight = [x.lower() for x in highlight]
            platform = platform.lower()
            data = ws_data(platform, lang, "fissures")
            embed = discord.Embed(
                            colour=self.colour,
                            timestamp=datetime.datetime.utcfromtimestamp(time.time())
                        )
            embed.set_author(
                        name=lang_pack["command_fissures_author_name"].format(platform.upper()),
                        url="https://warframe.fandom.com/wiki/Void_Fissure",
                        icon_url=ctx.guild.me.avatar_url
                    )
            for f in data:
                if f["active"]:
                    mission_type = f['missionType']
                    tier = f['tier']
                    faction = f['enemy']
                    if not len(highlight):
                        embed.add_field(
                                name=f"• **{mission_type}** - **{tier}** {f['eta']} " + lang_pack["time_left"],
                                value=f" **{f['node']}** - {faction}",
                                inline=False
                            )
                    else:
                        for h in highlight:
                            if h in mission_type.lower() or h in tier.lower() or \
                                h in faction.lower():
                                embed.add_field(
                                    name=f"• **{mission_type}** - **{tier}** {f['eta']} " + lang_pack["time_left"],
                                    value=f" **{f['node']}** - {faction}",
                                    inline=False
                                )
            embed.set_thumbnail(url=self.thumb_dev_comm)
            embed.set_footer(
                        text=self.footer_ws,
                        icon_url=ctx.guild.me.avatar_url
                    )
            await e_send(ctx, to_delete, embed=embed, delay=delay)
        elif platform is None:
            await e_send(ctx, to_delete, message=lang_pack["provide_platform"].format(ctx.author.mention), delay=delay)
        else:
            await e_send(ctx, to_delete, message=lang_pack["wrong_platform"].format(ctx.author.mention), delay=delay)

    @commands.command()
    @trigger_typing
    async def sortie(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        data = ws_data('pc', lang, 'sortie')
        embed = discord.Embed(
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time()),
            description=lang_pack["command_sortie_description"].format(data["faction"], data["eta"], data["boss"])
        )
        embed.set_author(
            name=lang_pack["command_sortie_author_name"],
            icon_url='https://vignette.wikia.nocookie.net/warframe/images/1/15/Sortie_b.png/revision/latest?cb=20151217134250'
            )
        embed.set_thumbnail(url=self.thumb_dev_comm)
        for c in data["variants"]:
            embed.add_field(
                name=f'• {c["missionType"]} - {c["node"]}',
                value=f'{c["modifier"]}', inline=False
                )
        embed.set_footer(
                text=self.footer_ws,
                icon_url=ctx.guild.me.avatar_url
                )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def arbitration(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        data = ws_data('pc', lang, 'arbitration')
        embed = discord.Embed(
            title=lang_pack["command_arbitration_title"],
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time()),
            description=arbitration_eta(data["expiry"])
        )
        embed.add_field(name=f"{data['type']} - {data['node']}", value=f"{data['enemy']}")
        embed.set_footer(
            text=self.footer_ws,
            icon_url=ctx.guild.me.avatar_url
            )
        embed.set_thumbnail(url=self.thumb_dev_comm)
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def baro(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        data = ws_data('pc', lang, 'voidTrader')
        if not len(data['inventory']):
            embed = discord.Embed(
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time()),
                description=lang_pack["command_baro_description_start"].format(data['startString'])
            )
            embed.set_author(
                name=lang_pack["command_baro_author_name"],
                icon_url='http://content.warframe.com/MobileExport/Lotus/Interface/Icons/Player/GlyphBaro.png'
                )

            embed.add_field(
                name=lang_pack["command_baro_field_name_location"],
                value=lang_pack["command_baro_field_value_location"].format(data['character'], data['location'])
                )
        else:
            embed = discord.Embed(
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time()),
                description=lang_pack["command_baro_description_end"].format(data['location'], data['endString'])
            )
            embed.set_author(
                name=lang_pack["command_baro_author_name"],
                icon_url='http://content.warframe.com/MobileExport/Lotus/Interface/Icons/Player/GlyphBaro.png'
                )
            embed.add_field(name=lang_pack["command_baro_field_name_location"], value=data['location'])
            for c in data['inventory']:
                embed.add_field(name=c['item'], value=str(c['ducats']) + '<:du:641336909989281842> + ' + str(c['credits']) + ' ' + lang_pack["credits"])
        embed.set_thumbnail(url=self.thumb_dev_comm)
        embed.set_footer(
            text=self.footer_ws,
            icon_url=ctx.guild.me.avatar_url
            )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def news(self, ctx, platform: str = None):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        if platform is not None and platform.lower() in ['pc', 'ps4', 'xb1', 'swi']:
            desc = ''
            data = ws_data(platform, lang, 'news')
            for c in reversed(data):
                desc += c['asString'] + '\n'
            embed = discord.Embed(
                title=lang_pack["command_news_title"].format(platform.upper()),
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time()),
                description=desc
                )
            embed.set_thumbnail(url=self.thumb_dev_comm)
            embed.set_footer(
            text=self.footer_ws,
                icon_url=ctx.guild.me.avatar_url
                )
            await e_send(ctx, to_delete, embed=embed, delay=delay)
        elif platform is None:
            await e_send(ctx, to_delete, message=lang_pack["provide_platform"].format(ctx.author.mention), delay=delay)
        else:
            await e_send(ctx, to_delete, message=lang_pack["wrong_platform"].format(ctx.author.mention), delay=delay)

    @commands.command()
    @trigger_typing
    async def earth(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        data = ws_data('pc', lang, 'earthCycle')
        lang_pack = locales(lang)
        timeLeft = data["timeLeft"]
        if timeLeft.startswith('-'):
            timeLeft = "0m:"
        if data["isDay"]:
            state = lang_pack["command_earth_to_night"]
            actual = "☀️"
        else:
            state = lang_pack["command_earth_to_day"]
            actual = "🌙"
        timeLeft += state
        embed = discord.Embed(
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time()),
            description=timeLeft
        )
        embed.set_author(name=lang_pack["command_earth_author_name"], icon_url="https://vignette.wikia.nocookie.net/warframe/images/1/1e/Earth.png/revision/latest?cb=20161016212227")
        embed.add_field(name=lang_pack["command_earth_field_name_state"], value=f"{data['state'].capitalize()} {actual}")
        embed.set_thumbnail(url=self.thumb_dev_comm)
        embed.set_footer(
                    text=self.footer_ws,
                    icon_url=ctx.guild.me.avatar_url
                )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def wiki(self, ctx, *wiki_query):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        base_uri = "https://warframe.fandom.com/wiki/"
        wiki_uri = '_'.join(x.capitalize() for x in wiki_query)
        embed = discord.Embed(
            title=f"{wiki_uri.replace('_', ' ')} Wiki",
            description=f"{base_uri + wiki_uri}",
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time())
        )
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/central/images/8/8d/FANDOM_heart.png/revision/latest?cb=20171003155851")
        embed.set_footer(
                    text=self.footer_ws,
                    icon_url=ctx.guild.me.avatar_url
                )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @staticmethod
    def _to_string_time(expiry) -> list:
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        de = datetime.datetime.strptime(expiry, f)
        da = datetime.datetime.now()
        delta = de - da
        days, seconds = delta.days, delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return days, hours, minutes, seconds

    @commands.command(aliases=["events"])
    @trigger_typing
    async def event(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        data = ws_data('pc', lang, 'events')
        embed = discord.Embed(
            title=lang_pack["command_event_title"],
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time())
        )
        embed.set_thumbnail(url=self.thumb_dev_comm)
        embed.set_footer(
                text=self.footer_ws,
                icon_url=ctx.guild.me.avatar_url
            )
        if len(data):
            for x in data:
                try:
                    embed.add_field(name='• ' + x['description'], value=x['asString'], inline=False)
                except:
                    continue
        else:
            embed.description = lang_pack["command_event_description_no_event"]
        return await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def nightwave(self, ctx):
        try:
            to_delete, delay, lang = read_settings(ctx.guild.id)
            lang_pack = locales(lang)
            uri_emblem = "https://vignette.wikia.nocookie.net/warframe/images/e/e0/NightwaveSyndicate.png/revision/latest?cb=20190727121305"
            data = ws_data('pc', lang, 'nightwave')
            days, hours, minutes, seconds = self._to_string_time(data['expiry'])
            days_p, hours_p, minutes_p, seconds_p = self._to_string_time(data['activeChallenges'][0]['expiry'])
            season_deadline = f"**{days}d {hours}h {minutes}mn {seconds}s**"
            challenges_deadline = f"**{days_p}d {hours_p}h {minutes_p}mn {seconds_p}s**"
            embed = discord.Embed(
                description=lang_pack["command_nightwave_description"].format(season_deadline, challenges_deadline).replace("-", ""),
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time())
            )
            embed.set_author(name=lang_pack["command_nightwave_author_name_actual_season"].format(data['season']), icon_url=uri_emblem)
            embed.set_thumbnail(url=self.thumb_dev_comm)
            embed.set_footer(
                    text=self.footer_ws,
                    icon_url=ctx.guild.me.avatar_url
                )
            for x in reversed(data['activeChallenges']):
                embed.add_field(name='• ' + x['title'], value=x['desc'] + f'\n**{x["reputation"]}** ' + lang_pack["reputation"], inline=False)
        except:
            return await e_send(ctx, to_delete, message=lang_pack["command_nightwave_no_nightwave"].format(ctx.author.mention), delay=delay)
        return await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def sentient(self, ctx):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        Tmp = ws_offi()['Tmp']
        if Tmp != '[]':
            Tmp = int(Tmp[7:10])
            embed = discord.Embed(
                title=lang_pack["command_sentient_title_active"],
                description=lang_pack["command_sentient_description_active"].format(sentient_node(Tmp)),
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time())
            )
            embed.add_field(
                name=lang_pack["command_sentient_field_name_note"],
                value=lang_pack["command_sentient_field_value_note"]
                )
        else:
            d = datetime.datetime.now()
            embed = discord.Embed(
                title=lang_pack["command_sentient_title_inactive"],
                description=lang_pack["command_sentient_description_inactive"].format(d.strftime("%Y-%m-%d %H:%M:%S")),
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time())
            )
            embed.add_field(
                name=lang_pack["command_sentient_field_name_note"],
                value=lang_pack["command_sentient_field_value_note"]
                )
        embed.set_thumbnail(url=self.thumb_dev_comm)
        embed.set_footer(
                text=self.footer_ws,
                icon_url=ctx.guild.me.avatar_url
            )
        return await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def fish(self, ctx, location):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        if location.lower() == "fortuna":
            embed = discord.Embed(
                title=lang_pack["command_fish_title_fortuna"],
                colour=self.colour,
            )
            embed.set_image(url="https://semlar.com/fishing_map8.jpg")
            embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP) | from semlar.com",
                    icon_url=ctx.guild.me.avatar_url
                )
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        if location.lower() == "cetus":
            to_delete, delay, lang = read_settings(ctx.guild.id)
            embed = discord.Embed(
                title=lang_pack["command_fish_title_cetus"],
                colour=self.colour,
            )
            embed.set_image(url="https://semlar.com/fishing_map.jpg")
            embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP) | from semlar.com",
                    icon_url=ctx.guild.me.avatar_url
                )
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        else:
            msg = lang_pack["command_fish_provide_valid_map"].format(ctx.author.mention)
            return await e_send(ctx, to_delete, message=msg, delay=delay)

    @commands.command()
    @trigger_typing
    async def acolytes(self):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        pass
    # @commands.command()
    # @trigger_typing
    # @commands.has_permissions(administrator=True)
    # async def track(self, ctx, track_command):
    #     VALID_TRACKER = ['sortie', 'baro', 'sentient']
    #     # to_delete, delay, lang = read_settings(ctx.guild.id)
    #     if track_command in VALID_TRACKER:
    #         channel = self.bot.get_channel(ctx.message.channel.id)
    #         await ctx.send(content=f"{ctx.message.channel.id} {channel}")
    #         await channel.send(content="yay")

def setup(bot):
    bot.add_cog(WorldState(bot))
