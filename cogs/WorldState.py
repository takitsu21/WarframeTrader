#!/usr/bin/env python3
#coding:utf-8

import discord, time, datetime
from discord.ext import commands
from src.worldstate import *
from src._discord import *

class WorldState(commands.Cog):
    """Warframe worldstate data"""
    def __init__(self,bot):
        self.bot = bot
        self.colour = 0x87DABC
        self.footer_ws = "Made with ❤️ by Taki#0853 (WIP) | using api.warframestat.us"

    @commands.command(aliases=["f"])
    async def fissures(self, ctx, platform: str = None):
        if platform is not None and platform.lower() in ["pc", "xb1", "ps4", "swi"]:
            platform = platform.lower()
            ws = WorldStateData()
            data = run(ws.data(platform, "fissures"))
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
                        text=self.footer_ws,
                        icon_url=ctx.guild.me.avatar_url
                    )
            await e_send(ctx, embed=embed, delay=300)
        elif platform is None:
            await ctx.send(f"{ctx.author.mention}Please provide a platform `<pc | ps4 | xb1 | swi>`")
        else:
            await ctx.send(f"{ctx.author.mention}Platform invalid!\nRetry with `*fissures <pc | ps4 | xb1 | swi>`")

    @commands.command(aliases=["a"])
    async def alerts(self, ctx, platform: str = None):
        if platform is not None and platform.lower() in ["pc", "xb1", "ps4", "swi"]:
            platform = platform.lower()
            ws = WorldStateData()
            data = run(ws.data(platform, "alerts"))
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
                        text=self.footer_ws,
                        icon_url=ctx.guild.me.avatar_url
                    )
            await e_send(ctx, embed=embed, delay=10)
        elif platform is None:
            await ctx.send(f"{ctx.author.mention}Please provide a platform `<pc | ps4 | xb1 | swi>`")
        else:
            await ctx.send(f"{ctx.author.mention}Platform invalid!\nRetry with `*fissures <pc | ps4 | xb1 | swi>`")


def setup(bot):
    bot.add_cog(WorldState(bot))
