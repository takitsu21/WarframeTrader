#!/usr/bin/env python3
# coding:utf-8
import discord
import datetime
import time
import os
from discord.ext import commands
from src.graphical_rendering import *
from src.wf_market_responses import *
from src.decorators import trigger_typing
from src.sql import *
from src._discord import *


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

    def generate_msg(self, ctx, to_delete, delay, fargs):
        msg = f"{ctx.author.mention}"
        if to_delete:
            if delay >= 60:
                msg += f"\nThe graph of {fargs} will be deleted in {round(delay/60, 2)} mins"
            else:
                msg += f"\nThe graph of {fargs} will be deleted in {delay} seconds"
        else:
            msg += f" You can see the graph of {fargs} below"
        return msg

    @commands.command(aliases=["st"])
    @trigger_typing
    async def stats(self, ctx, *args):
        to_delete, delay = read_settings(ctx.guild.id)
        if len(args):
            try:
                args_endpoint = '_'.join(args).lower()
                capitalize_args = [x.capitalize() for x in args]
                fargs = ' '.join(capitalize_args)
                graphs_path = f"./graphs/{args_endpoint}.png"
                self.make_graph(args_endpoint, fargs)
                msg = self.generate_msg(ctx, to_delete, delay, fargs)           
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
                    title='❌Error❌',
                    colour=0xFF0026,
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    description="You might have spelled a wrong item name 🤔"
                )
                embed.set_thumbnail(url='https://warframe.market/static/assets/frontend/logo_icon_only.png')
                embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP) | api.warframe.market",
                    icon_url=ctx.guild.me.avatar_url
                )
                await e_send(ctx, to_delete, embed=embed, delay=delay)

def setup(bot):
    bot.add_cog(Statistics(bot))
