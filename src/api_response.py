#!/usr/bin/python
#coding:utf-8
import json, os, asyncio, nest_asyncio
from aiohttp import ClientSession


nest_asyncio.apply()#fix asyncio error


class StatusError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


def set_headers():
    with open("../config.json", "r") as f:
        config = json.load(f)["headers"]
    headers = {
        "Authorization":config["token"],
        "Platform":config["platform"],
        "Language":config["language"]
        }
    return headers

class WfmApi:
    """Returns warframe.market data"""
    def __init__(self, *endpoints : list):
        self.icon_root = "https://warframe.market/static/assets/" #Example : https://warframe.market/static/assets/icons/en/thumbs/Akbronco_Prime_Set.34b5a7f99e5f8c15cc2039a76c725069.128x128.png
        self.root = "https://api.warframe.market/v1/"
        self.headers = set_headers()
        self.endpoints = '/'.join(endpoints)
        self.URL = f"{self.root}{self.endpoints}"

    async def fetch(self, session):
        """make requests"""
        async with session.get(self.URL, headers=self.headers) as r:
            try:
                assert r.status == 200
                return await r.json()
            except:
                raise StatusError(r.status)
    

    async def data(self) -> dict:
        """returns api.warframe.market responses -> dict"""
        async with ClientSession() as session:
            responses = await self.fetch(session)
        return responses
    
    async def icon_endpoint(self, icon: bool=True) -> str:
        async with ClientSession() as session:
            responses = await self.fetch(session)
        return self.icon_root + [x["icon"] for x in responses["payload"]["item"]["items_in_set"]][0] if icon else \
            self.icon_root + [x["thumb"] for x in responses["payload"]["item"]["items_in_set"]][0]
 

def run(func = lambda x: x):
    """asyncio runner function using python 3.7"""
    return asyncio.run(func)
 

def check_status(status: str) -> int:
    return {"ingame":3, "online":2,"offline":1}[status]

def order_type_convert(order_type :str) -> str:
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
            prices[order["user"]["ingame_name"]] = {"status":order["user"]["status"],
                                                    "rep":order["user"]["reputation"],
                                                    "platinum":order["platinum"],
                                                    "quantity":order["quantity"],
                                                    "order_type":order["order_type"]}
            list_to_sort.append((order["user"]["ingame_name"],
                                order["platinum"]))
    list_to_sort = sorted(list_to_sort, key=lambda v : v[1])
    for igname, p in list_to_sort:
        parser.append({"status":prices[igname]["status"],
                                "name":igname,
                                "rep":prices[igname]["rep"],
                                "platinum":p,
                                "quantity":prices[igname]["quantity"],
                                "order_type":prices[igname]["order_type"],
                                "number":i})
        if i == 10:
            break
        i+=1
    _sorted["data"] = parser
    return _sorted

# if __name__ == "__main__":
#     api = WfmApi("items", "ash_prime_blueprint", "statistics")
#     print(json.dumps(run(api.data()), indent=4))