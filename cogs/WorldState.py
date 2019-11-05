#!/usr/bin/env python3
# coding:utf-8
import discord
import time
import datetime
from discord.ext import commands
from src.worldstate import *
from src._discord import *


class WorldState(commands.Cog):
    """Warframe worldstate data"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC
        self.footer_ws = "Made with ❤️ by Taki#0853 (WIP) | using api.warframestat.us | will be deleted in "

    @commands.command(aliases=["f"])
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
                            name=f"• **{f['missionType']}** - **{f['tier']}** *{f['eta']}* remaining",
                            value=f" **{f['node']}** - *{f['enemy']}*",
                            inline=False
                        )
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(
                        text=self.footer_ws + str(delay) + "s",
                        icon_url=ctx.guild.me.avatar_url
                    )
            await e_send(ctx, embed=embed, delay=delay)
        elif platform is None:
            await ctx.send(f"{ctx.author.mention}Please provide a platform `<pc | ps4 | xb1 | swi>`")
        else:
            await ctx.send(f"{ctx.author.mention}Platform invalid!\nRetry with `*fissures <pc | ps4 | xb1 | swi>`")

    @commands.command()
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
                text=self.footer_ws + str(delay) + "s",
                icon_url=ctx.guild.me.avatar_url
                )
        await e_send(ctx, embed=embed, delay=delay)

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
