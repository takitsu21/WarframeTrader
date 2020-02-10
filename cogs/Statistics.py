#!/usr/bin/env python3
# coding:utf-8
import discord
import datetime
import time
import os, sys
from discord.ext import commands
from src.graphical_rendering import *
from src.wf_market_responses import *
from src.decorators import trigger_typing
from src.sql import *
from src._discord import *
from src.util import locales


class Statistics(commands.Cog):
    """Graphical Stats for an item"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC

    @staticmethod
    def make_graph(args_endpoint: str, fargs: str):
        api = WfmApi("pc", "items", args_endpoint, "statistics")
        graph = GraphProcess(fargs, args_endpoint)
        graph.save_graph(api.data())

    @commands.command(aliases=["st"])
    @trigger_typing
    async def stats(self, ctx, *args):
        to_delete, delay, lang = read_settings(ctx.guild.id)
        lang_pack = locales(lang)
        if len(args):
            try:
                args_endpoint = '_'.join(args).lower()
                capitalize_args = [x.capitalize() for x in args]
                fargs = ' '.join(capitalize_args)
                graphs_path = f"./graphs/{args_endpoint}.png"
                self.make_graph(args_endpoint, fargs)
                msg = lang_pack["command_stat_msg_title"].format(ctx.author.mention, fargs)
                with open(graphs_path, 'rb') as p:
                    if delay:
                        await ctx.message.delete(delay=delay)
                    await ctx.send(
                        msg,
                        file=discord.File(p, graphs_path),
                        delete_after=delay
                        )
                os.remove(graphs_path)
            except Exception as e:
                print(f"{type(e).__name__} : {e}")
                embed = discord.Embed(
                    title=lang_pack["error"],
                    colour=0xFF0026,
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    description=lang_pack["wrong_item_name"]
                )
                embed.set_thumbnail(url='https://warframe.market/static/assets/frontend/logo_icon_only.png')
                embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP) | api.warframe.market",
                    icon_url=ctx.guild.me.avatar_url
                )
                await e_send(ctx, to_delete, embed=embed, delay=delay)

def setup(bot):
    bot.add_cog(Statistics(bot))
