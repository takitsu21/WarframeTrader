#!/usr/bin/python
#coding:utf-8
import json, os, asyncio
from aiohttp import ClientSession

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

    async def fetch(self, session) -> str:
        """make requests"""
        async with session.get(self.URL, headers=self.headers) as r:
            try:
                assert r.status == 200
                return await r.json()
            except:
                raise StatusError(await r.json(), r.status)
    

    async def data(self) -> str:
        """returns api.warframe.market responses"""
        async with ClientSession() as session:
            responses = await self.fetch(session)
        return responses
    
    async def icon_endpoint(self, icon: bool=True) -> str:
        async with ClientSession() as session:
            responses = await self.fetch(session)
        return [x["icon"] for x in responses["payload"]["item"]["items_in_set"]][0] if icon else \
            [x["thumb"] for x in responses["payload"]["item"]["items_in_set"]][0]
 

def run(func = lambda x: x):
    """asyncio runner function"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(func)
 

def check_status(status) -> int:
    if status == "ingame": return 3
    return 2 if status == "online" else 1
 
def sort_orders(data) -> dict:
    _sorted, prices = {}, {}
    list_to_sort = []
    parser = []
    for order in data["payload"]["orders"]:
        # if order["user"]["status"] == "ingame":
        if order["user"]["status"] == "ingame":
            prices[order["user"]["ingame_name"]] = {"status":order["user"]["status"],
                                                    "rep":order["user"]["reputation"],
                                                    "platinum":order["platinum"],
                                                    "quantity":order["quantity"],
                                                    "icon":order["icon"]}
            list_to_sort.append((order["user"]["ingame_name"],
                                order["platinum"],
                                order["user"]["status"]))
    list_to_sort = sorted(list_to_sort, key=lambda v : v[1])
    list_to_sort = sorted(list_to_sort, key=lambda v : v[2], reverse=True)
    for igname, p, st in list_to_sort:
        parser.append({"status":prices[igname]["status"],
                                "name":igname,
                                "rep":prices[igname]["rep"],
                                "platinum":prices[igname]["platinum"],
                                "quantity":prices[igname]["quantity"]})
    _sorted["data"] = parser
    return _sorted

def show_listed_orders(orders : dict):
    for _data in orders["data"]:
        print("{} | {} +{}rep -> {}pl --- {} qt".format(_data["name"],
                        _data["status"],
                        _data["rep"],
                        _data["platinum"],
                        _data["quantity"]))

if __name__ == "__main__":
    api = WfmApi("items", "condition_overload")
    print(json.dumps(run(api.icon_endpoint(icon=False)), indent=4))