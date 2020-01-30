import discord
import time
import datetime
from discord.ext import commands
import asyncio
import logging
import aiohttp


logger = logging.getLogger('warframe')


class Tracker(commands.Cog):
    """Tracker"""
    pass
    # def __init__(self, bot):
    #     self.bot = bot
    #     self.colour = 0x87DABC
    #     self.updating = self.bot.loop.create_task(self.update_ws())


    # async def update_ws(self):
    #     while not self.bot.is_closed():

    #         await asyncio.sleep(60)

def setup(bot):
    global logger
    logger = logging.getLogger('warframe')
    bot.add_cog(Tracker(bot))