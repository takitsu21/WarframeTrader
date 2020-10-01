# import discord
# import time
# import datetime
# from discord.ext import commands
# from src.worldstate import *
# from src._discord import *
# from src.decorators import trigger_typing
# from src.sql import all_lobbys, insert_player_lobby, get_lobby, create_lobby


# WARFRAME_LIST = [
#     'ash',
#     'atlas',
#     'banshee',
#     'baruuk',
#     'chroma',
#     'ember',
#     'equinox',
#     'excalibur',
#     'frost',
#     'gara',
#     'garuda',
#     'gauss',
#     'grendel',
#     'harrow',
#     'hildryn',
#     'hydroid',
#     'inaros',
#     'ivara',
#     'khora',
#     'limbo',
#     'loki',
#     'mag',
#     'mesa',
#     'mirage',
#     'nekros',
#     'nezha',
#     'nidus',
#     'nova',
#     'nyx',
#     'oberon',
#     'octavia',
#     'revenant',
#     'rhino',
#     'saryn',
#     'titania',
#     'trinity',
#     'valkyr',
#     'vauban',
#     'volt',
#     'wisp',
#     'wukong',
#     'zephyrash prime',
#     'atlas prime',
#     'banshee prime',
#     'chroma prime',
#     'ember prime',
#     'equinox prime',
#     'excalibur prime',
#     'frost prime',
#     'hydroid prime',
#     'limbo prime',
#     'loki prime',
#     'mag prime',
#     'mesa prime',
#     'mirage prime',
#     'nekros prime',
#     'nova prime',
#     'nyx prime',
#     'oberon prime',
#     'rhino prime',
#     'saryn prime',
#     'trinity prime',
#     'valkyr prime',
#     'vauban prime',
#     'volt prime',
#     'wukong prime',
#     'zephyr prime'
# ]


# class Lobby(commands.Cog):
#     """
#     Lobby handler
#     """
#     pass
#     # def __init__(self, bot):
#     #     self.bot = bot
#     #     self.colour = 0x87DABC

#     # def parse_lobby(args):
#     #     lobbuffer = []
#     #     data = {"lobbys":lobbuffer}
#     #     lobbys = all_lobbys()
#     #     l = ('id', 'lobbyname', 'lobbykey',
#     #          'mode', 'player1', 'player2',
#     #          'player3', 'player4', 'tagplayer1',
#     #          'tagplayer2', 'tagplayer3', 'tagplayer4',
#     #          'activation', 'expiry')
#     #     for lobby in lobbys:
#     #         zz = zip(lobby, l)
#     #         # print(list())
#     #         parser = {
#     #             "name": getattr(zz, 'lobbyname')
#     #         }
#     #         print(parser)


#     # def lobby_embed(self, ctx, lobby_data):
#     #     pass

#     # @commands.command()
#     # @trigger_typing
#     # async def lobby(self, ctx, *, args):
#     #     if not len(args):
#     #         pass


# def setup(bot):
#     bot.add_cog(Lobby(bot))