#!/usr/bin/python3
# coding:utf-8
import requests
from src.exceptions import *

class WfmApi:
    """
    Returns warframe.market data
    """
    def __init__(self, platform: str, *endpoints: list):
        self.icon_root = "https://warframe.market/static/assets/"  # Example : https://warframe.market/static/assets/icons/en/thumbs/Akbronco_Prime_Set.34b5a7f99e5f8c15cc2039a76c725069.128x128.png
        self.root = "https://api.warframe.market/v1/"
        self.endpoints = '/'.join(endpoints)
        self.URL = f"{self.root}{self.endpoints}"
        self.platform = platform

    def data(self):
        """
        Fetch data from warframe market
        """
        HEADERS = {
            "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiI1MnpmU3daV1RBYTNsOUFkdWswU2RDSkI1UlRtWUpkdSIsImNzcmZfdG9rZW4iOiI3YzI2YzNkMjE0NGZmNGZlNjZhYTE3YzczMTUwODJkNjdmZGEzYjE5IiwiZXhwIjoxNTY1MzQ3MjEyLCJpYXQiOjE1NjAxNjMyMTIsImlzcyI6Imp3dCIsImF1ZCI6Imp3dCIsImF1dGhfdHlwZSI6ImNvb2tpZSIsInNlY3VyZSI6ZmFsc2UsImp3dF9pZGVudGl0eSI6InBMc0RiQU9wS2hoMkMwRzNZeVlVcXZ1Q1FtQk5kMGVBIiwibG9naW5fdWEiOiJiJ01vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS83NC4wLjM3MjkuMTY5IFNhZmFyaS81MzcuMzYnIiwibG9naW5faXAiOiJiJzJhMDE6ZTM1OjJlYTg6YTJjMDpkZGQzOjFiMzQ6MTQ0MDo5Y2UnIn0.Lon4TLmsk5fx6MltPCMY11ONUZT3dKeyMVkfR81p8n4",
            "Platform": self.platform,
            "Language": "en"
        }
        r = requests.get(self.URL, headers=HEADERS)
        if r.status_code == 200:
            return r.json()
        raise StatusError(r)

    def icon_endpoint(self, icon: bool = True) -> str:
        responses = self.data()
        return self.icon_root + [x["icon"] for x in responses["payload"]["item"]["items_in_set"]][0] if icon else \
               self.icon_root + [x["thumb"] for x in responses["payload"]["item"]["items_in_set"]][0]

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
        if i == 9:
            break
        i += 1
    _sorted["data"] = parser
    return _sorted
