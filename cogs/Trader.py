#!/usr/bin/env python3
# coding:utf-8
import discord
import datetime
import time
from discord.ext import commands
from src.wf_market_responses import *
from src._discord import *
from src.exceptions import *
from src.decorators import trigger_typing
from src.sql import *


class Trader(commands.Cog):
    """Trader commands"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x87DABC

    def embed_exceptions(self, ctx, command, description: list=[]):
        prefix = read_prefix(ctx.guild.id)
        command = f"{prefix}{command}"
        embed = discord.Embed(
            title=command,
            color=self.colour,
            description='\n'.join(list((f"`{command} {x}`") for x in description)),
            timestamp=datetime.datetime.utcfromtimestamp(time.time())
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(
            text="Made with ❤️ by Taki#0853 (WIP)",
            icon_url=ctx.guild.me.avatar_url
        )
        return embed

    @commands.command(aliases=["b"])
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def wtb(self, ctx, platform: str=None, *args):
        to_delete, delay = read_settings(ctx.guild.id)
        if platform is None:
            embed = self.embed_exceptions(ctx, "wtb", description=["<pc | xbox | ps4 | swi> [ITEM_NAME]"])
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        try:
            platform = platform.lower()
            if platform in ["pc", "xbox", "ps4", "swi"]:
                args_endpoint = '_'.join(args).lower()
                api_orders = WfmApi(platform, "items", args_endpoint, "orders")
                api_icons = WfmApi(platform, "items", args_endpoint)
                item_data = sort_orders(api_orders.data(), "wtb")
                item_thumb = api_icons.icon_endpoint(args_endpoint)
                capitalize_args = [x.capitalize() for x in args]
                formatted_args = ' '.join(capitalize_args)
                prefix = read_prefix(ctx.guild.id)
                embed = discord.Embed(
                    title=f'💰WTB {formatted_args}💰\n<:_purple_circle:643936797222764554> Online in game - Sort by prices',
                    colour=self.colour,
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    description=f"View grapghical stats ↙️\n**`{prefix}stats {' '.join(args)}`**"
                )

                if len(item_data["data"]):
                    for i, d in enumerate(item_data["data"], start=1):
                        pl = int(d["platinum"])
                        embed.add_field(
                            name="{0}. **{1}** | "
                                 "+**{2}**🙂 for **{3}** <:pl:632332600538824724> x "
                                 "**{4}** pieces".format(i, d["name"], d["rep"], pl, d["quantity"]),
                            value="||`/w {0} Hi! I want to buy: {1} "
                                  "for {2} platinum. (warframe.market - https://top.gg/bot/593364281572196353)`||"
                                  .format(d["name"], formatted_args, pl), inline=False
                        )
                else:
                    embed.add_field(
                            name="0 offer for {}".format(formatted_args),
                            value="No one is actually online in game sorry!\nComeback later tenno!"
                        )
                embed.set_thumbnail(url=item_thumb)
                embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP) | api.warframe.market",
                    icon_url=ctx.guild.me.avatar_url
                )
            else:
                embed = self.embed_exceptions(ctx, "wtb", description=["<pc | xbox | ps4 | swi> [ITEM_NAME]"])
                return await e_send(ctx, to_delete, embed=embed, delay=delay)
        except StatusError as e:
            embed = discord.Embed(
                    title='❌Error❌',
                    colour=0xFF0026,
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    description=f"{type(e).__name__} : ERROR {e} (You might have spelled a wrong item name or the API is down)`🤔`"
                )
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(
                text="Made with ❤️ by Taki#0853 (WIP) | api.warframe.market",
                icon_url=ctx.guild.me.avatar_url
            )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(aliases=["s"])
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def wts(self, ctx, platform: str=None, *args):
        to_delete, delay = read_settings(ctx.guild.id)
        if platform is None:
            embed = self.embed_exceptions(ctx, "wts", description=["<pc | xbox | ps4 | swi> [ITEM_NAME]"])
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        try:
            platform = platform.lower()
            if platform in ["pc", "xbox", "ps4", "swi"]:
                args_endpoint = '_'.join(args).lower()
                api_orders = WfmApi(platform, "items", args_endpoint, "orders")
                api_icons = WfmApi(platform, "items", args_endpoint)
                item_data = sort_orders(api_orders.data(), "wts")
                item_thumb = api_icons.icon_endpoint(args_endpoint)
                capitalize_args = [x.capitalize() for x in args]
                formatted_args = ' '.join(capitalize_args)
                prefix = read_prefix(ctx.guild.id)
                embed = discord.Embed(
                    title=f'💰WTS {formatted_args}💰\n<:_purple_circle:643936797222764554> Online in game - Sort by prices',
                    colour=self.colour,
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    description=f"View grapghical stats ↙️\n**`{prefix}stats {' '.join(args)}`**"
                )
                if len(item_data["data"]):
                    for i, d in enumerate(item_data["data"], start=1):
                        pl = int(d["platinum"])
                        embed.add_field(
                            name="{0}. **{1}** | "
                                 "+**{2}**🙂 for **{3}** <:pl:632332600538824724> x "
                                 "**{4}** pieces".format(i, d["name"], d["rep"], pl, d["quantity"]),
                            value="||`/w {0} Hi! I want to sell: {1} "
                                  "for {2} platinum. (warframe.market - https://top.gg/bot/593364281572196353)`||"
                                  .format(d["name"], formatted_args, pl)
                        )
                else:
                    embed.add_field(
                            name="0 offer for {}".format(formatted_args),
                            value="No one is actually online in game sorry!\nComeback later tenno!"
                        )
                embed.set_thumbnail(url=item_thumb)
                embed.set_footer(
                    text="Made with ❤️ by Taki#0853 (WIP) | api.warframe.market",
                    icon_url=ctx.guild.me.avatar_url
                )
            else:
                embed = self.embed_exceptions(ctx, "wts", description=["<pc | xbox | ps4 | swi> [ITEM_NAME]"])
                return await e_send(ctx, to_delete, embed=embed, delay=delay)
        except StatusError as e:
            embed = discord.Embed(
                    title='❌Error❌',
                    colour=0xFF0026,
                    timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                    description=f"{type(e).__name__} : ERROR {e} (You might have spelled a wrong item name or the API is down)🤔"
                )
            embed.set_thumbnail(url='https://warframe.market/static/assets/frontend/logo_icon_only.png')
            embed.set_footer(
                text="Made with ❤️ by Taki#0853 (WIP) | api.warframe.market",
                icon_url=ctx.guild.me.avatar_url
            )
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @commands.command(aliases=["d"])
    @trigger_typing
    @commands.bot_has_permissions(manage_messages=True)
    async def ducats(self, ctx):
        to_delete, delay = read_settings(ctx.guild.id)
        ducats = WfmApi('pc', 'tools', 'ducats')
        items = WfmApi('pc', 'items')
        ducats_data = ducats.data()
        items_data = items.data()
        embed = discord.Embed(
            timestamp=datetime.datetime.utcfromtimestamp(time.time()),
            colour=self.colour
        )
        embed.set_author(
            name="Ducanator",
            icon_url='https://image.winudf.com/v2/image1/Y29tLm1vcmhhbS5kdWNhdHNvcHRpbWl6ZXJfaWNvbl8xNTQxNTI1NjY3XzA2MA/icon.png?w=170&fakeurl=1'
            )
        embed.set_thumbnail(url='https://warframe.market/static/assets/frontend/logo_icon_only.png')
        for i, du in enumerate(ducats_data['payload']['previous_day'], start=1):
            for x in items_data['payload']['items']:
                if x['id'] == du['item']:
                    embed.add_field(
                        name=f"{i}. {x['item_name']}",
                        value=f'**{du["ducats_per_platinum_wa"]}** <:du:641336909989281842>/<:pl:632332600538824724>\n**{du["wa_price"]}** WA Price\n**{du["ducats"]}** <:du:641336909989281842>'
                    )
                    continue
            if i == 18:
                break
        embed.set_footer(
            text="Made with ❤️ by Taki#0853 (WIP) | api.warframe.market",
            icon_url=ctx.guild.me.avatar_url
        )         
        await e_send(ctx, to_delete, embed=embed, delay=delay)

    @staticmethod
    def convert_polarity(polarity_name: str):
        return {
            'madurai': '<:madurai:643915728818405396>',
            'naramon': '<:naramon:643915707364409354>',
            'vazarin': '<:vazarin:643848307348602905>'
            }[polarity_name]

    @staticmethod
    def convert_status(status: str):
        d = {
            'offline': ('<:_red_circle:643936812527779850>', 'Offline'),
            'online': ('<:_green_circle:643936852327530548>', 'Online'),
            'ingame': ('<:_purple_circle:643936797222764554>', 'Online in game')
        }[status]
        return d[0], d[1]

    @commands.command(aliases=["r"])
    @commands.bot_has_permissions(manage_messages=True)
    async def riven(self, ctx, platform: str = None, *args):
        to_delete, delay = read_settings(ctx.guild.id)
        if platform is None:
            embed = self.embed_exceptions(ctx, "riven", description=["<pc | xbox | ps4 | swi> [ITEM_NAME]"])
            return await e_send(ctx, to_delete, embed=embed, delay=delay)
        elif platform in ["pc", "xbox", "ps4", "swi"]:
            try:
                args = [x.lower() for x in args]
                fargs = '_'.join(args)
                auction_query = WfmApi(platform, 'auctions', f'search?type=riven&weapon_url_name={fargs}&polarity=any&sort_by=price_asc')
                data = auction_query.data()
                if len(data['payload']['auctions']):
                    embed = discord.Embed(
                        description=f"<:_green_circle:643936852327530548> Online | Online in game <:_purple_circle:643936797222764554>",
                        timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                        colour=self.colour
                    )
                    item_c = ' '.join(args).capitalize()
                    embed.set_author(name=f"Riven auctions for {item_c}", url='https://warframe.fandom.com/wiki/Riven_Mods', icon_url='http://content.warframe.com/MobileExport/Lotus/Interface/Cards/Images/OmegaMod.png')
                    attributes = '```diff\n'
                    i = 0
                    for auction_iter in data['payload']['auctions']:
                        if auction_iter['owner']['status'] in ["ingame", "online"]:
                            status_emoji, status_game = self.convert_status(auction_iter['owner']['status'])
                            embed.add_field(
                                name=f"**{item_c} {auction_iter['item']['name']}** {status_emoji}",
                                value=f"Buyout price {auction_iter['buyout_price']} | Starting price {auction_iter['starting_price']} | Top bid {auction_iter['top_bid']}\nPolarity {self.convert_polarity(auction_iter['item']['polarity'])} | MR {auction_iter['item']['mastery_level']}\nRe-rolls {auction_iter['item']['re_rolls']} | Mod rank {auction_iter['item']['mod_rank']}\n[View Riven](https://warframe.market/auction/{auction_iter['id']})\n|| `/w {auction_iter['owner']['ingame_name']} Hi!` ||",
                                inline=False
                            )
                            for attribute in auction_iter['item']['attributes']:
                                attr = attribute['url_name'].replace('_', ' ')
                                if attribute['positive']:
                                    attributes += f"+ {attribute['value']} {attr}\n"
                                else:
                                    value = abs(attribute['value'])
                                    attributes += f"- {value} {attr}\n"
                                
                            attributes += '\n```'
                            embed.add_field(name='Attributes', value=attributes, inline=False)
                            attributes = '```diff\n'
                            if i == 5:
                                break
                            i += 1

                    embed.set_footer(
                        text="Made with ❤️ by Taki#0853 (WIP) | api.warframe.market",
                        icon_url=ctx.guild.me.avatar_url
                    )
                    embed.set_thumbnail(url='https://warframe.market/static/assets/frontend/logo_icon_only.png')
                    await e_send(ctx, to_delete, embed=embed, delay=delay)
                else:
                    embed = discord.Embed(
                        description="There is actually no offer sorry! Come back later Tenno!",
                        timestamp=datetime.datetime.utcfromtimestamp(time.time()),
                        colour=self.colour
                    )
                    embed.set_author(name=f"Riven auctions for {item_c}", url='https://warframe.fandom.com/wiki/Riven_Mods', icon_url='http://content.warframe.com/MobileExport/Lotus/Interface/Cards/Images/OmegaMod.png')
                    embed.set_footer(
                        text="Made with ❤️ by Taki#0853 (WIP) | api.warframe.market",
                        icon_url=ctx.guild.me.avatar_url
                    )
                    await e_send(ctx, to_delete, embed=embed, delay=delay)
            except StatusError:
                embed = self.embed_exceptions(ctx, "riven", description=["<pc | xbox | ps4 | swi> [ITEM_NAME]"])
                await e_send(ctx, to_delete, embed=embed, delay=delay)
        else:
            embed = self.embed_exceptions(ctx, "riven", description=["<pc | xbox | ps4 | swi> [ITEM_NAME]"])
            await e_send(ctx, to_delete, embed=embed, delay=delay)

def setup(bot):
    bot.add_cog(Trader(bot))
