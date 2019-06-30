#!/usr/bin/env python3
#coding:utf-8

import discord, datetime, time, os 
from discord.ext import commands
from src.graphical_rendering import *
from src.wf_market_responses import * 


class Statistics(commands.Cog):
    """Trader commands"""
    def __init__(self,bot):
        self.bot = bot
        self.colour = 0x87DABC

    def make_graph(self, args: str, args_endpoint: str) -> bytes:
        api = WfmApi("pc","items", args_endpoint, "statistics")
        capitalize_args = [x.capitalize() for x in args]
        formatted_args = ' '.join(capitalize_args)
        graph = GraphProcess(formatted_args, args_endpoint)
        graph.save_graph(run(api.data()))

    def get_file_time(self, file_path):
        return datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

    @commands.command(pass_context=True)
    async def stats(self, ctx, *args):
        today = datetime.datetime.now()
        args_endpoint = '_'.join(args).lower()
        graphs_path = "graphs/"+args_endpoint+".png"
        try:
            if os.path.exists(graphs_path):
                file_date = self.get_file_time(graphs_path)
                if file_date.day == today.day:
                    pass
                else:
                    self.make_graph(args, args_endpoint)
            else:
                self.make_graph(args, args_endpoint)
        except Exception as e:
            print(f"{type(e).__name__} : {e}")
            return
        finally:
            with open(graphs_path, 'rb') as p:
                await ctx.send(file=discord.File(p,
                    graphs_path))
            


def setup(bot):
    bot.add_cog(Statistics(bot))
    print("Added Statistics")