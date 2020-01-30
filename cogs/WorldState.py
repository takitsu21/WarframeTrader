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
    async def fissures(self, ctx, platform: str=None):
        to_delete, delay = read_settings(ctx.guild.id)
        if platform is not None and platform.lower() in ["pc", "xb1", "ps4", "swi"]:
            platform = platform.lower()
            data = ws_data(platform, "fissures")
            embed = discord.Embed(
                            colour=self.colour,
                            timestamp=datetime.datetime.utcfromtimestamp(time.time())
                        )
            embed.set_author(
                        name=f"[{platform.upper()}] - Fissures",
                        url="https://warframe.fandom.com/wiki/Void_Fissure",
                        icon_url=ctx.guild.me.avatar_url
                    )
            for f in data:
                if f["active"]:
                    embed.add_field(
                            name=f"• **{f['missionType']}** - **{f['tier']}** {f['eta']} remaining",
                            value=f" **{f['node']}** - {f['enemy']}",
                            inline=False
                        )
            embed.set_thumbnail(url=self.thumb_dev_comm)
            embed.set_footer(
                        text=self.footer_ws,
                        icon_url=ctx.guild.me.avatar_url
                    )
            await e_send(ctx, to_delete, embed=embed, delay=delay)
        elif platform is None:
            await e_send(ctx, to_delete, message=f"{ctx.author.mention} Please provide a platform `<pc | ps4 | xb1 | swi>`", delay=delay)
        else:
            await e_send(ctx, to_delete, message=f"{ctx.author.mention} Platform invalid!\nRetry with `*fissures <pc | ps4 | xb1 | swi>`", delay=delay)

    @commands.command()
    @trigger_typing
    async def sortie(self, ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        data = ws_data('pc', 'sortie')
        embed = discord.Embed(
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time()),
            description=f'Faction : **{data["faction"]}**\nTime left **{data["eta"]}**\n In-progress : **{data["boss"]}**'
        )
        embed.set_author(
            name='Sortie',
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
        to_delete, delay = read_settings(ctx.guild.id)
        data = ws_data('pc', 'arbitration')
        embed = discord.Embed(
            title='Arbitration',
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
        to_delete, delay = read_settings(ctx.guild.id)
        data = ws_data('pc', 'voidTrader')
        if not len(data['inventory']):
            embed = discord.Embed(
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time()),
                description='start in ' + '**' + data['startString'] + '**'
            )
            embed.set_author(
                name="Baro Ki'Teer",
                icon_url='http://content.warframe.com/MobileExport/Lotus/Interface/Icons/Player/GlyphBaro.png'
                )
            embed.add_field(name='Location', value=data['character'] + ' will be at ' + data['location'])
        else:
            embed = discord.Embed(
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time()),
                description='end in ' + '**' + data['endString'] + '**'
            )
            embed.set_author(
                name="Baro Ki'Teer",
                icon_url='http://content.warframe.com/MobileExport/Lotus/Interface/Icons/Player/GlyphBaro.png'
                )
            embed.add_field(name='Location', value=data['location'])
            for c in data['inventory']:
                embed.add_field(name=c['item'], value=str(c['ducats']) + '<:du:641336909989281842> + ' + str(c['credits']) + ' credits')
        embed.set_thumbnail(url=self.thumb_dev_comm)
        embed.set_footer(
            text=self.footer_ws,
            icon_url=ctx.guild.me.avatar_url
            )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def news(self, ctx, platform: str = None):
        to_delete, delay = read_settings(ctx.guild.id)
        if platform is not None and platform.lower() in ['pc', 'ps4', 'xb1', 'swi']:
            desc = ''
            data = ws_data(platform, 'news')
            for c in reversed(data):
                desc += c['asString'] + '\n'
            embed = discord.Embed(
                title=f'Warframe News [{platform.upper()}]',
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
            await e_send(ctx, to_delete, message=f"{ctx.author.mention} Please provide a platform `<pc | ps4 | xb1 | swi>`", delay=delay)
        else:
            await e_send(ctx, to_delete, message=f"{ctx.author.mention} Platform invalid!\nRetry with `*news <pc | ps4 | xb1 | swi>`", delay=delay)

    @commands.command()
    @trigger_typing
    async def earth(self, ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        data = ws_data('pc', 'earthCycle')
        timeLeft = data["timeLeft"]
        if timeLeft.startswith('-'):
            timeLeft = "0m:"
        if data["isDay"]:
            state = " to night 🌙"
            actual = "☀️"
        else:
            state = " to day ☀️"
            actual = "🌙"
        timeLeft += state
        embed = discord.Embed(
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time()),
            description=timeLeft
        )
        embed.set_author(name="Earth Cycle", icon_url="https://vignette.wikia.nocookie.net/warframe/images/1/1e/Earth.png/revision/latest?cb=20161016212227")
        embed.add_field(name="State", value=f"{data['state'].capitalize()} {actual}")
        embed.set_thumbnail(url=self.thumb_dev_comm)
        embed.set_footer(
                    text=self.footer_ws,
                    icon_url=ctx.guild.me.avatar_url
                )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def wiki(self, ctx, *wiki_query):
        to_delete, delay = read_settings(ctx.guild.id)
        base_uri = "https://warframe.fandom.com/wiki/"
        wiki_uri = '_'.join(x.capitalize() for x in wiki_query)
        embed = discord.Embed(
            title=f"{wiki_uri.replace('_', ' ')} Wiki",
            description=f"{base_uri + wiki_uri}",
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time())
        )
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/central/images/8/8d/FANDOM_heart.png/revision/latest?cb=20171003155851""https://vignette.wikia.nocookie.net/central/images/8/8d/FANDOM_heart.png/revision/latest?cb=20171003155851")
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
        to_delete, delay = read_settings(ctx.guild.id)
        data = ws_data('pc', 'events')
        embed = discord.Embed(
            title=f"Current Events",
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
            embed.description = 'There is no events for now\nCome back later tenno!'
        return await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def nightwave(self, ctx):
        try:
            to_delete, delay = read_settings(ctx.guild.id)
            uri_emblem = "https://vignette.wikia.nocookie.net/warframe/images/e/e0/NightwaveSyndicate.png/revision/latest?cb=20190727121305"
            data = ws_data('pc', 'nightwave')
            days, hours, minutes, seconds = self._to_string_time(data['expiry'])
            days_p, hours_p, minutes_p, seconds_p = self._to_string_time(data['activeChallenges'][0]['expiry'])
            embed = discord.Embed(
                description=f'This season expire in **{days}d {hours}h {minutes}mn {seconds}s**\n'
                            f'Week challenges expire in **{days_p}d {hours_p}h {minutes_p}mn {seconds_p}s**'.replace('-', ''),
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time())
            )
            embed.set_author(name=f"Nightwave season {data['season']}", icon_url=uri_emblem)
            embed.set_thumbnail(url=self.thumb_dev_comm)
            embed.set_footer(
                    text=self.footer_ws,
                    icon_url=ctx.guild.me.avatar_url
                )
            for x in reversed(data['activeChallenges']):
                embed.add_field(name='• ' + x['title'], value=x['desc'] + f'\n**{x["reputation"]}** reputation', inline=False)
        except:
            return await e_send(ctx, to_delete, message=f"{ctx.author} There is no nightwave operation for now!", delay=delay)
        return await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def sentient(self, ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        Tmp = ws_offi()['Tmp']
        if Tmp != '[]':
            Tmp = int(Tmp[7:10])
            embed = discord.Embed(
                title="Sentient ship active",
                description="Sentient ship on {}".format(sentient_node(Tmp)),
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time())
            )
            embed.add_field(
                name="NOTE",
                value="When the sentient ship appear you will see" \
                      " the planet concerned on the bot activity"\
                      " beside cetus and fortuna cycle's datas"
                )
        else:
            d = datetime.datetime.now()
            embed = discord.Embed(
                title="Sentient ship inactive",
                description="Last update {} GMT +0000".format(d.strftime("%Y-%m-%d %H:%M:%S")),
                colour = self.colour,
                timestamp = datetime.datetime.utcfromtimestamp(time.time())
            )
            embed.add_field(
                name="NOTE",
                value="If sentient ship appear you will see" \
                      " the planet concerned on the bot activity"\
                      " beside cetus and fortuna cycle's datas"
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
        to_delete, delay = read_settings(ctx.guild.id)
        if location.lower() == "fortuna":
            embed = discord.Embed(
                title="Fortuna fishing map",
                colour=self.colour,
            )
            embed.set_image(url="https://semlar.com/fishing_map8.jpg")
            embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP) | from semlar.com",
                    icon_url=ctx.guild.me.avatar_url
                )
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        if location.lower() == "cetus":
            to_delete, delay = read_settings(ctx.guild.id)
            embed = discord.Embed(
                title="Cetus fishing map",
                colour=self.colour,
            )
            embed.set_image(url="https://semlar.com/fishing_map.jpg")
            embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP) | from semlar.com",
                    icon_url=ctx.guild.me.avatar_url
                )
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        else:
            msg = f"{ctx.author.mention} Please provide a valid map location like `fortuna` or `cetus`"
            return await e_send(ctx, to_delete, message=msg, delay=delay)

    # @commands.command()
    # @trigger_typing
    # @commands.has_permissions(administrator=True)
    # async def track(self, ctx, track_command):
    #     VALID_TRACKER = ['sortie', 'baro', 'sentient']
    #     # to_delete, delay = read_settings(ctx.guild.id)
    #     if track_command in VALID_TRACKER:
    #         channel = self.bot.get_channel(ctx.message.channel.id)
    #         await ctx.send(content=f"{ctx.message.channel.id} {channel}")
    #         await channel.send(content="yay")

def setup(bot):
    bot.add_cog(WorldState(bot))
