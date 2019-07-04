#!/usr/bin/python3
#coding:utf-8
import discord, os, asyncio, logging
from discord.ext import commands
from cogs import *
from src.worldstate import *

__version__ = "0.0.1"
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

cyan = 0x87DAB
client = commands.Bot(command_prefix='*', activity=discord.Game(name='Updating...'),
                      status=discord.Status('idle'), afk=True)

with open("commands.txt", "r") as f:
    help_commands = ''.join(f.readlines())

def get_cetusCycle(data: dict) -> str:
    if "-" in data["timeLeft"]:
        return None
    timeLeft = data["timeLeft"].split(" ")[0]
    if data["isDay"]:
        string = timeLeft + " to ☀️"
    else:
        string = timeLeft + " to 🌙"
    return string

@client.event
async def on_disconnect():
    print(f"{client.user.name} succesfully disconnected")

@client.event
async def on_guild_join(ctx):
    embed = discord.Embed(title='**Nice to meet you!**',
                        colour=cyan,
                        description= "Thanks for inviting me!")
    embed.add_field(name="**Prefix**", value="`*`")
    embed.add_field(name="**About Warframe Trader**",
                    value="Type `*help` to get all the commands!")
    embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)")
    await ctx.owner.send(embed = embed)

@client.event
async def on_member_join(ctx):
    embed = discord.Embed(title='**Welcome to the server!**',
                        colour=cyan,
                        description="Hey tenno 👋 try to trade with me on Warframe!")
    embed.add_field(name="Commands",value=help_commands)
    embed.set_thumbnail(url=ctx.guild.me.avatar_url)
    embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                    icon_url=ctx.guild.me.avatar_url)
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    #waiting internal cache to be ready
    await client.wait_until_ready()
    client.remove_command("help")

    loaded = None
    fail = str()
    # Adding Cogs
    for file in os.listdir("cogs/"):
        try:
            if file.endswith(".py"):
                client.load_extension(f'cogs.{file.split(".")[0]}')
        except Exception as e:
            print(f"{file} can't be loaded :\n {type(e).__name__} : {e}")
            fail += file + " "
            loaded = False
    if loaded is None:
        print('All cogs loaded!')
    else: print(f"Cogs missing -> {fail}")
    # nb_users, t, acc = 0,0,0
    ws = WorldState()
    while True:
        cetus_string = get_cetusCycle(run(ws.data("pc", "cetusCycle")))
        await client.change_presence(
            activity=discord.Activity(name="[*help] {0}".format(cetus_string),
            type=3)
            )
        await asyncio.sleep(60)

client.run()

