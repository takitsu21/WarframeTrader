#!/usr/bin/python3
# coding:utf-8
from src.exceptions import *
from decouple import config

from aiohttp import ClientSession

class WfmApi():
    """
    Returns warframe.market data
    """
    __slots__ = (
        "icon_root",
        "root",
        "endpoints",
        "URL",
        "platform",
        "session"
    )
    def __init__(self, session: ClientSession, platform: str, *endpoints: list):
        self.icon_root = "https://warframe.market/static/assets/"  # Example : https://warframe.market/static/assets/icons/en/thumbs/Akbronco_Prime_Set.34b5a7f99e5f8c15cc2039a76c725069.128x128.png
        self.root = "https://api.warframe.market/v1/"
        self.endpoints = '/'.join(endpoints)
        self.URL = f"{self.root}{self.endpoints}"
        self.platform = platform
        self.session = session

    async def data(self):
        """
        Fetch data from warframe market
        """
        HEADERS = {
            "Authorization": f"JWT {config('jwt')}",
            "Platform": self.platform,
            "Language": "en"
        }
        r = await self.session.get(self.URL, headers=HEADERS)
        if r.status == 200:
            return await r.json()
        raise StatusError(r.status)

    async def icon_endpoint(self, url_name) -> str:
        responses = await self.data()
        try:
            for x in responses["payload"]["item"]["items_in_set"]:
                if url_name == x["url_name"]:
                    return self.icon_root + x["sub_icon"]
        except:
            return self.icon_root + responses["payload"]["item"]["items_in_set"][0]["thumb"]

def check_status(status: str) -> int:
    return {"ingame": 3, "online": 2, "offline": 1}[status]

def order_type_convert(order_type: str) -> str:
    if order_type == "wts":
        return "buy"
    elif order_type == "wtb":
        return "sell"

def sort_orders(data: dict, order_type: str) -> dict:
    _sorted, prices = {}, {}
    list_to_sort = []
    parser = []
    i = 0
    for order in data["payload"]["orders"]:
        if order["user"]["status"] == "ingame" and order["order_type"] == order_type_convert(order_type):
            prices[order["user"]["ingame_name"]] = {
                "status": order["user"]["status"],
                "rep": order["user"]["reputation"],
                "platinum": order["platinum"],
                "quantity": order["quantity"],
                "order_type": order["order_type"]
                }
            list_to_sort.append((order["user"]["ingame_name"],
                                order["platinum"]))
    list_to_sort = sorted(list_to_sort, key=lambda v: v[1])
    for igname, p in list_to_sort:
        parser.append({
            "status": prices[igname]["status"],
            "name": igname,
            "rep": prices[igname]["rep"],
            "platinum": p,
            "quantity": prices[igname]["quantity"],
            "order_type": prices[igname]["order_type"],
            "number": i
            })
        if i == 6:
            break
        i += 1
    _sorted["data"] = parser
    return _sorted