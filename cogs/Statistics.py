#!/usr/bin/env python3
#coding:utf-8

import discord, datetime, time, os 
from discord.ext import commands
from src.graphical_rendering import *
from src.api_response import * 
class Statistics(commands.Cog):
    """Trader commands"""
    def __init__(self,bot):
        self.bot = bot
        self.colour = 0x87DABC

    @commands.command(pass_context=True)
    async def stats(self, ctx, *args):
        args_endpoint = '_'.join(args).lower()
        api = WfmApi("items", args_endpoint, "statistics")
        capitalize_args = [x.capitalize() for x in args]
        formatted_args = ' '.join(capitalize_args)
        graph = GraphProcess(formatted_args, args_endpoint)
        graph.save_graph(run(api.data()))
        with open("graphs/"+args_endpoint+".png", 'rb') as p:
            await ctx.send(file=discord.File(p,
            "graphs/"+args_endpoint+".png"))


def setup(bot):
    bot.add_cog(Statistics(bot))
    print("Added Statistics")