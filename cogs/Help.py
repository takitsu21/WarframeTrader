#!/usr/bin/env python3
#coding:utf-8

import discord
from discord.ext import commands

help_commands = """`*help` - returns help commands
`*wtb <item_name>` - returns items on sale""" 

class Help(commands.Cog):
    """Help commands"""
    def __init__(self,bot):
        self.bot = bot
        self.colour = 0x87DABC

    @commands.command(pass_context=True)
    async def help(self,ctx):
        embed = discord.Embed(title='**Supported Commands**',
                            colour=self.colour)
        embed.add_field(name="Commands",value=help_commands)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text="Made by Taki#0853 (WIP)",
                        icon_url=ctx.guild.me.avatar_url)
        await ctx.author.send(embed=embed)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Help(bot))
    print("Added Help")