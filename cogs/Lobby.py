import discord
import time
import datetime
from discord.ext import commands
from src.worldstate import *
from src._discord import *
from src.decorators import trigger_typing
from src.sql import *


WARFRAME_LIST = [
    'ash',
    'atlas', 
    'banshee', 
    'baruuk', 
    'chroma', 
    'ember', 
    'equinox', 
    'excalibur', 
    'frost', 
    'gara', 
    'garuda', 
    'gauss', 
    'grendel', 
    'harrow', 
    'hildryn', 
    'hydroid', 
    'inaros', 
    'ivara', 
    'khora', 
    'limbo', 
    'loki', 
    'mag', 
    'mesa', 
    'mirage', 
    'nekros', 
    'nezha', 
    'nidus', 
    'nova', 
    'nyx', 
    'oberon', 
    'octavia', 
    'revenant', 
    'rhino', 
    'saryn', 
    'titania', 
    'trinity', 
    'valkyr', 
    'vauban', 
    'volt', 
    'wisp', 
    'wukong', 
    'zephyrash prime', 
    'atlas prime', 
    'banshee prime', 
    'chroma prime', 
    'ember prime', 
    'equinox prime', 
    'excalibur prime', 
    'frost prime', 
    'hydroid prime', 
    'limbo prime', 
    'loki prime', 
    'mag prime', 
    'mesa prime', 
    'mirage prime', 
    'nekros prime', 
    'nova prime', 
    'nyx prime', 
    'oberon prime', 
    'rhino prime', 
    'saryn prime', 
    'trinity prime', 
    'valkyr prime', 
    'vauban prime', 
    'volt prime', 
    'wukong prime', 
    'zephyr prime'
]


class Lobby(commands.Cog):
    """
    Lobby handler
    """
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC

    # @commands.command()
    # @trigger_typing
    # async def lobby(self, ctx, *, args):
    #     if not len(args):
    #         pass

def setup(bot):
    bot.add_cog(Lobby(bot))