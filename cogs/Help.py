#!/usr/bin/env python3
#coding:utf-8

import discord
from discord.ext import commands

class Help(commands.Cog):
    """Help commands"""
    def __init__(self,bot):
        self.bot = bot
        self.colour = 0x87DABC

    @classmethod
    def commands_verison(cls, settings):
        if settings is None:
            version = "Commands"
            with open("commands.txt", "r",encoding="utf8") as f:
                lines = f.readlines()
        elif settings == "--s":
            version = "Shorter version commands"
            with open("commands_s.txt", "r",encoding="utf8") as f:
                lines = f.readlines()
        return ''.join(lines), version


    @commands.command(aliases=["h"])
    async def help(self, ctx, settings = None):
        comm = self.commands_verison(settings)
        embed = discord.Embed(
                        title='**Supported Commands**',
                        colour=self.colour
                        )
        embed.add_field(name=comm[1],value=comm[0])
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        await ctx.author.send(embed=embed)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Help(bot))
    print("Added Help")