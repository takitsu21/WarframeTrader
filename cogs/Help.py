#!/usr/bin/env python3
# coding:utf-8

import discord
import time
from discord.ext import commands
from src.decorators import trigger_typing


class Help(commands.Cog):
    """Help commands"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC

    @commands.command()
    @trigger_typing
    async def ping(self,ctx):
        """Ping's Bot"""
        before = time.monotonic()
        message = await ctx.send("🏓Pong!")
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(colour=0xff00,
                            title="Apex Stats ping",
                            description=f"🏓{int(ping)} ms")
        await message.edit(content="", embed=embed)

    @commands.command(aliases=["h"])
    @trigger_typing
    async def help(self, ctx, settings=None):
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Help(bot))
