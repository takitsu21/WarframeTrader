#!/usr/bin/env python3
# coding:utf-8
import discord
import datetime
import time
import os
from discord.ext import commands
from src.graphical_rendering import *
from src.wf_market_responses import *


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

    @staticmethod
    def get_file_time(file_path: str):
        return datetime.datetime.fromtimestamp(
                    os.path.getmtime(file_path)
               )

    def clean_dir(self, path, today):
        if os.path.exists(path+"flag"):
            if self.get_file_time(path+"flag").day == today.day:
                return True
            else:
                for file in os.listdir(path):
                    os.remove(file)
                open("flag", "a").close()
                return False
        open(path+"flag", "a").close()
        return False

    def embed_graph(self, ctx, item_name, icon):
        embed = discord.Embed(
            title=f"{item_name} Graphic",
            timestamp=datetime.datetime.utcfromtimestamp(time.time()),
            description="Will be deleted in 5 mins!",
            colour=self.colour
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Made with ❤️ by Taki#0853 (WIP) | using api.warframe.market",
            icon_url=ctx.guild.me.avatar_url
        )
        return embed

    @commands.command(aliases=["st"])
    async def stats(self, ctx, *args):
        args_endpoint = '_'.join(args).lower()
        thumb = WfmApi("pc", "items", args_endpoint)
        capitalize_args = [x.capitalize() for x in args]
        fargs = ' '.join(capitalize_args)
        graphs_path = "graphs/"+args_endpoint+".png"
        try:
            if os.path.exists(graphs_path):
                today = datetime.datetime.now()
                if self.clean_dir("graphs/", today):
                    pass
                else:
                    self.make_graph(args_endpoint, fargs)
            else:
                self.make_graph(args_endpoint, fargs)
        except Exception as e:
            print(f"{type(e).__name__} : {e}")
            return
        finally:
            embed = self.embed_graph(ctx, fargs, thumb.icon_endpoint())
            with open(graphs_path, 'rb') as p:
                await ctx.send(
                    embed=embed,
                    file=discord.File(p, graphs_path),
                    delete_after=300
                    )
            await ctx.message.delete(delay=300)


def setup(bot):
    bot.add_cog(Statistics(bot))
