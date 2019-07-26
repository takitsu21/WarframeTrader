#!/usr/bin/env python3
# coding:utf-8
import discord
import datetime
import time
from discord.ext import commands
from src.wf_market_responses import *
from src._discord import *
from src.exceptions import *


class Trader(commands.Cog):
    """Trader commands"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC

    @commands.command(aliases=["b"])
    async def wtb(self, ctx, platform: str=None, *args):
        if platform is None:
            return await ctx.send(f"{ctx.author.mention}Please provide a platform `<pc | xbox | ps4>`")
        try:
            platform = platform.lower()
            if platform in ["pc", "xbox", "ps4"]:
                embed = discord.Embed(
                    title='`💰`Items on sale`💰` (Online in game - Sort by prices)',
                    colour=self.colour,
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    description=f"Will be deleted in 5 minutes!\nYou can get stats with the following command\n**`*stats {' '.join(args)}`**"
                )
                args_endpoint = '_'.join(args).lower()
                api_orders = WfmApi(platform, "items", args_endpoint, "orders")
                api_icons = WfmApi(platform, "items", args_endpoint)
                item_data = sort_orders(run(api_orders.data()), "wtb")
                item_thumb = run(api_icons.icon_endpoint())
                capitalize_args = [x.capitalize() for x in args]
                formatted_args = ' '.join(capitalize_args)
                if len(item_data["data"]):
                    for i, d in enumerate(item_data["data"], start=1):
                        pl = int(d["platinum"])
                        embed.add_field(
                            name="`{0}.` **{1}** *Online in game* "\
                                "+**{2}**`🙂` **{3}** platinum "\
                                "**{4}** pieces".format(i, d["name"], d["rep"], pl, d["quantity"]),
                            value="||`/w {0} Hi! I want to buy: {1} "\
                                "for {2} platinum. (warframe.market - Warframe Trader bot)`||"\
                                .format(d["name"], formatted_args, pl)
                        )
                else:
                    embed.add_field(
                            name="0 offer for {}".format(formatted_args),
                            value="No one is actually online in game sorry!\nComeback later tenno!"
                        )
                embed.set_thumbnail(url=item_thumb)
                embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP) | using api.warframe.market",
                    icon_url=ctx.guild.me.avatar_url
                )
            else:
                return await ctx.send(f"{ctx.author.mention}Wrong platform try with `<pc | xbox | ps4>`")
        except StatusError as e:
            embed = discord.Embed(
                    title='❌Error❌',
                    colour=0xFF0026,
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    description=f"{type(e).__name__} : ERROR {e} (You might have spelled a wrong item name or the API is down)`🤔`"
                )
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(
                text="Made with ❤️ by Taki#0853 (WIP) | using api.warframe.market",
                icon_url=ctx.guild.me.avatar_url
            )
        await e_send(ctx, embed=embed, delay=300)


def setup(bot):
    bot.add_cog(Trader(bot))
