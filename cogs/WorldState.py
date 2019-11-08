#!/usr/bin/env python3
# coding:utf-8
import discord
import time
import datetime
from discord.ext import commands
from src.worldstate import *
from src._discord import *
from src.decorators import trigger_typing


class WorldState(commands.Cog):
    """Warframe worldstate data"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC
        self.footer_ws = "Made with ❤️ by Taki#0853 (WIP) | using api.warframestat.us"

    @commands.command(aliases=["f"])
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def fissures(self, ctx, platform: str=None):
        if platform is not None and platform.lower() in ["pc", "xb1", "ps4", "swi"]:
            delay = 300
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
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(
                        text=self.footer_ws,
                        icon_url=ctx.guild.me.avatar_url
                    )
            await e_send(ctx, embed=embed, delay=delay)
        elif platform is None:
            await e_send(ctx, message=f"{ctx.author.mention} Please provide a platform `<pc | ps4 | xb1 | swi>`", delay=60)
        else:
            await e_send(ctx, message=f"{ctx.author.mention} Platform invalid!\nRetry with `*fissures <pc | ps4 | xb1 | swi>`", delay=60)

    @commands.command()
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def sortie(self, ctx):
        delay = 300
        data = ws_data('pc', 'sortie')
        embed = discord.Embed(
            title='Sortie',
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time()),
            description=f'Faction : **{data["faction"]}**\nTime left **{data["eta"]}**'
        )
        embed.set_author(
            name='Sortie',
            icon_url='https://vignette.wikia.nocookie.net/warframe/images/1/15/Sortie_b.png/revision/latest?cb=20151217134250'
            )
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        for i, c in enumerate(data["variants"], start=1):
            embed.add_field(
                name=f'• __Part {i}__',
                value=f'**{c["missionType"]}** mission on **{c["node"]}**'
                      f'\n**{c["modifierDescription"]}**'
                )
        embed.set_footer(
                text=self.footer_ws,
                icon_url=ctx.guild.me.avatar_url
                )
        await e_send(ctx, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def arbitration(self, ctx):
        delay = 300
        data = ws_data('pc', 'arbitration')
        embed = discord.Embed(
            title='Arbitration',
            colour = self.colour,
            timestamp = datetime.datetime.utcfromtimestamp(time.time()),
            description=arbitration_eta(data["expiry"])
            # description=f'Mission type : **{data["type"]}**\nFaction : **{data["enemy"]}**\n{arbitration_eta(data["expiry"])}\n{data["node"]}'
        )
        embed.add_field(name="Mission Type", value=f"{data['type']}")
        embed.add_field(name='Node', value=f"{data['node']}")
        embed.add_field(name='Faction', value=f'{data["enemy"]}')
        embed.set_footer(
            text=self.footer_ws,
            icon_url=ctx.guild.me.avatar_url
            )
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        await e_send(ctx, embed=embed, delay=delay)
    
    @commands.command()
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def baro(self, ctx):
        delay = 600
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
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(
            text=self.footer_ws,
            icon_url=ctx.guild.me.avatar_url
            )
        await e_send(ctx, embed=embed, delay=delay)

    @commands.command()
    @trigger_typing
    async def news(self, ctx, platform: str = None):
        if platform is not None and platform.lower() in ['pc', 'ps4', 'xb1', 'swi']:
            delay = 300
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
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(
                text=self.footer_ws,
                icon_url=ctx.guild.me.avatar_url
                )
            await e_send(ctx, embed=embed, delay=delay)
        elif platform is None:
            await e_send(ctx, message=f"{ctx.author.mention} Please provide a platform `<pc | ps4 | xb1 | swi>`", delay=60)
        else:
            await e_send(ctx, message=f"{ctx.author.mention} Platform invalid!\nRetry with `*news <pc | ps4 | xb1 | swi>`", delay=60)
    # @commands.command(aliases=["a"])
    # async def alerts(self, ctx, platform: str=None):
    #     if platform is not None and platform.lower() in ["pc", "xb1", "ps4", "swi"]:
    #         platform = platform.lower()
    #         data = ws_data(platform, "alerts")
    #         embed = discord.Embed(
    #                         colour=self.colour,
    #                         timestamp=datetime.datetime.utcfromtimestamp(time.time())
    #                     )
    #         embed.set_author(
    #                     name=f"[{platform.upper()}] - Fissures",
    #                     url="https://warframe.fandom.com/wiki/Void_Fissure",
    #                     icon_url=ctx.guild.me.avatar_url
    #                 )
    #         for f in data:
    #             if f["active"]:
    #                 embed.add_field(
    #                         name=f"• **{f['missionType']}** - **{f['tier']}** *{f['eta']}* remaining",
    #                         value=f" **{f['node']}** - *{f['enemy']}*",
    #                         inline=False
    #                     )
    #         embed.set_thumbnail(url=ctx.guild.me.avatar_url)
    #         embed.set_footer(
    #                     text=self.footer_ws,
    #                     icon_url=ctx.guild.me.avatar_url
    #                 )
    #         await e_send(ctx, embed=embed, delay=10)
    #     elif platform is None:
    #         await ctx.send(f"{ctx.author.mention}Please provide a platform `<pc | ps4 | xb1 | swi>`")
    #     else:
    #         await ctx.send(f"{ctx.author.mention}Platform invalid!\nRetry with `*fissures <pc | ps4 | xb1 | swi>`")


def setup(bot):
    bot.add_cog(WorldState(bot))
