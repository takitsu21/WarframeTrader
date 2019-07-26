#!/usr/bin/python3
# coding:utf-8
import discord
import os
import asyncio
import logging
from discord.ext import commands
from cogs import *
from src.worldstate import *


__version__ = "0.0.1"
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
        filename='discord.log',
        encoding='utf-8',
        mode='w'
    )
handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
        )
    )
logger.addHandler(handler)

cyan = 0x87DAB
client = commands.Bot(
            command_prefix='*',
            activity=discord.Game(name='Updating...'),
            status=discord.Status('idle'),
            afk=True
        )

with open("commands.txt", "r", encoding="utf8") as f:
    lines = f.readlines()
    help_commands = ''.join(lines)


def ttc_c(time, icon_type):
    if time is None:
        return None
    new_t = time.split(" ")
    new_t_lenght = len(new_t)
    if new_t_lenght == 1:
        return time + icon_type
    minute_time = 60 if new_t_lenght - 2 == 1 or "h" in new_t[0] else 0
    min_sum = str()
    for x in new_t[new_t_lenght - 2]:
        try: min_sum += x if isinstance(int(x), int) else ""
        except Exception as e: logger.error(e)
    minute_time += int(min_sum)
    return str(minute_time) + "m" + icon_type


def get_cetusCycle(data: dict) -> list:
    timeLeft = data["timeLeft"]
    if "-" in timeLeft:
        return None
    if data["isDay"]:
        icon = " to 🌙"
    else:
        icon = " to ☀️"
    return timeLeft, icon


def get_orbisCycle(data: dict) -> list:
    timeLeft = data["timeLeft"]
    if "-" in timeLeft:
        return None
    if data["isWarm"]:
        icon = " to ❄️"
    else:
        icon = " to 🔥"
    return timeLeft, icon


@client.event
async def on_guild_join(ctx):
    embed = discord.Embed(
                    title='**Nice to meet you!**',
                    colour=cyan,
                    description="Thanks for inviting me!"
                )
    embed.add_field(name="**Prefix**", value="`*`")
    embed.add_field(name="**About Warframe Trader**",
                    value="Type `*help` to get all the commands!")
    embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)")
    await ctx.owner.send(embed=embed)


@client.event
async def on_member_join(ctx):
    embed = discord.Embed(
            title='**Welcome to the server!**',
            colour=cyan,
            description="Hey tenno 👋 try to trade with me on Warframe!"
            )
    embed.add_field(name="Commands", value=help_commands)
    embed.set_thumbnail(url=ctx.guild.me.avatar_url)
    embed.set_footer(
                text="Made with ❤️ by Taki#0853 (WIP)",
                icon_url=ctx.guild.me.avatar_url
                )
    await ctx.send(embed=embed)


@client.event
async def on_ready():
    # waiting internal cache to be ready
    await client.wait_until_ready()
    client.remove_command("help")
    loaded = None
    fail = str()
    # Adding Cogs
    for file in os.listdir("cogs/"):
        try:
            if file.endswith(".py"):
                client.load_extension(f'cogs.{file.split(".")[0]}')
                print(f"{file} loaded")
        except Exception as e:
            print(f"{file} can't be loaded :\n {type(e).__name__} : {e}")
            fail += file + " "
            loaded = False
    if loaded is None:
        print('All cogs loaded!')
    else: print(f"Cogs missing -> {fail}")
    ws = WorldStateData()
    while True:
        try:
            vallis_time = get_orbisCycle(run(ws.data("pc", "vallisCycle")))
            cetus_time = get_cetusCycle(run(ws.data("pc", "cetusCycle")))
            cetus_string = ttc_c(cetus_time[0], cetus_time[1])
            vallis_string = ttc_c(vallis_time[0], vallis_time[1])
        except Exception as e:
            logger.error(e)
            cetus_string = ""
            vallis_string = ""
        await client.change_presence(
            activity=discord.Activity(
                name="{0} | {1} [*help]".format(cetus_string, vallis_string),
                type=3
                )
            )
        await asyncio.sleep(60)

client.run("")
