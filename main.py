#!/usr/bin/python3
# coding:utf-8
import discord
import os
import asyncio
import logging
from discord.ext import commands
from src.worldstate import *
import decouple
from discord.ext.commands import when_mentioned_or
import datetime
import time
from discord.utils import find
from src.sql import *
from aiohttp import ClientSession
import nest_asyncio
nest_asyncio.apply()

__version__ = "0.0.1"
logger = logging.getLogger('warframe')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
        filename='warframe.log',
        encoding='utf-8',
        mode='w'
    )
handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
        )
    )
logger.addHandler(handler)

API_WARFRAME_STAT = "https://api.warframestat.us/"

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
        except Exception: pass
    minute_time += int(min_sum)
    return str(minute_time) + "m:" + icon_type

def get_cetusCycle(data: dict) -> list:
    timeLeft = data["timeLeft"]
    if timeLeft.startswith('-'):
        timeLeft = "0m:"
    if data["isDay"]:
        icon = "🌙"
    else:
        icon = "☀️"
    return timeLeft, icon

def get_orbisCycle(data: dict) -> list:
    timeLeft = data["timeLeft"]
    if timeLeft.startswith('-'):
        timeLeft = '0m:'
    if data["isWarm"]:
        icon = "❄️"
    else:
        icon = "🔥"
    return timeLeft, icon

async def fetcher():
    urls = [
            API_WARFRAME_STAT + "pc/cetusCycle",
            API_WARFRAME_STAT + "pc/vallisCycle",
            "http://content.warframe.com/dynamic/worldState.php"
            ]
    tasks = []
    async with ClientSession() as session:
        for u in urls:
            task = asyncio.ensure_future(fetch(session, u))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses
    return responses

def _get_prefix(bot, message):
    try:
        prefix = read_prefix(message.guild.id)
        return when_mentioned_or(prefix)(bot, message)
    except Exception as e:
        logger.exception(e, exc_info=True)
        return when_mentioned_or('*')(bot, message)

class WarframeTrader(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=_get_prefix,
            activity=discord.Game(name='Updating...'),
            status=discord.Status('dnd')
        )
        self.remove_command("help")
        self._load_extensions()
        self.colour = 0x87DAB

    def _load_extensions(self):
        for file in os.listdir("cogs/"):
            try:
                if file.endswith(".py"):
                    self.load_extension(f'cogs.{file[:-3]}')
                    logger.info(f"{file} loaded")
            except Exception:
                logger.exception(f"Fail to load {file}")

    def _unload_extensions(self):
        for file in os.listdir("cogs/"):
            try:
                if file.endswith(".py"):
                    self.unload_extension(f'cogs.{file[:-3]}')
                    logger.info(f"{file} unloaded")
            except Exception:
                logger.exception(f"Fail to unload {file}")

    async def on_guild_remove(self, guild: discord.Guild):
        d_guild(guild.id)
        logger.info(f"guild {guild.id} removed")

    async def on_guild_join(self, guild: discord.Guild):
        try:
            i_guild_settings(guild.id, '*', 0, None)
            logger.info(f"guild {guild.id} added")
        except Exception as e:
            logger.exception(e, exc_info=True)
        general = find(lambda x: x.name == "general", guild.text_channels)
        embed = discord.Embed(
                        title='**Nice to meet you!**',
                        colour=self.colour,
                        description="Thanks for inviting me!"
                    )
        embed.add_field(name="Prefix", value="`*`")
        embed.add_field(name="About Warframe Trader",
                        value="Type `*help` to get all commands!")
        embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)")
        await guild.owner.send(embed=embed)
        if general and general.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                    title="Nice to meet you!",
                    description="Below are the infos about Warframe Trader",
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    color=self.colour
                )
            embed.set_thumbnail(url=guild.me.avatar_url)
            # embed.add_field(name="Vote",
            #                 value="[Click here](https://discordbots.org/bot/551446491886125059/vote)")
            embed.add_field(name="Invite Warframe Trader",
                            value="[Click here](https://discordapp.com/oauth2/authorize?client_id=593364281572196353&scope=bot&permissions=470083648)")
            embed.add_field(name="Discord Support",
                            value="[Click here](https://discordapp.com/invite/wTxbQYb)")
            embed.add_field(name="Donate",value="[Patreon](https://www.patreon.com/takitsu)\n[Kofi](https://ko-fi.com/takitsu)")
            embed.add_field(name = "Source code and commands", value="[Click here](https://takitsu21.github.io/WarframeTrader/)")
            embed.add_field(name="Help command",value="*help")
            embed.add_field(name="Default prefix",value="*")
            nb_users = 0
            for s in self.guilds:
                nb_users += len(s.members)

            embed.add_field(name="Servers", value=len(self.guilds))
            embed.add_field(name="Members", value=nb_users)
            embed.add_field(name="**Creator**", value="Taki#0853")
            embed.set_footer(text="Made with ❤️ by Taki#0853 (WIP)",
                            icon_url=guild.me.avatar_url)
            await general.send(embed=embed)

    async def on_ready(self):
        # waiting internal cache to be ready
        await self.wait_until_ready()
        while True:
            try:
                responses = asyncio.run(fetcher()).result()
                c = responses.pop(0) # Cetus cycle
                cetus_time = get_cetusCycle(c)
                cetus_string = ttc_c(cetus_time[0], cetus_time[1])
                c = responses.pop(0) # Fortuna cycle
                vallis_time = get_orbisCycle(c)
                vallis_string = ttc_c(vallis_time[0], vallis_time[1])
                c = responses.pop(0)['Tmp'] # Sentient ship
                node = ""
                if c != '[]':
                    code = int(Tmp[7:10])
                    node = sentient_node(code) + " | "
            except Exception as e:
                logger.exception(e, exc_info=True)
            try:
                await self.change_presence(
                    activity=discord.Activity(
                        name="{0}{1} | {2} | [*help] & [@Mention help]".format(node, cetus_string, vallis_string),
                        type=3
                        )
                    )
            except:
                await self.change_presence(
                    activity=discord.Activity(
                        name="Synchronization... | [*help] & [@Mention help]",
                        type=3
                        )
                    )
            await asyncio.sleep(60)

    def run(self, *args, **kwargs):
        try:
            self.loop.run_until_complete(self.start(decouple.config("debug_token")))
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())
            for task in asyncio.all_tasks(self.loop):
                task.cancel()
            try:
                self.loop.run_until_complete(
                    asyncio.gather(*asyncio.all_tasks(self.loop))
                )
            except asyncio.CancelledError:
                logger.debug("Pending tasks has been cancelled.")
            finally:
                try:
                    conn.close()
                    logger.info("Connection closed")
                except Exception as e:
                    logger.exception(e, exc_info=True)
                logger.info("Shutting down")

if __name__ == "__main__":
    bot = WarframeTrader()
    bot.run()
