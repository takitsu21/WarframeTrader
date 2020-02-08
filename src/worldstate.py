import requests
from src.exceptions import *
import datetime
import os
import json


ROOT = "https://api.warframestat.us/"
FORMAT_DATE = "%Y-%m-%dT%H:%M:%S.%fZ"

# async def fetch(session, url):
#     async with session.get(url) as r:
#         txt = await r.text()
#         loaded = json.loads(txt)
#         return loaded

def ws_data(platform: str="pc", *endpoints: list) -> dict:
    endpoint = platform + "/" + '/'.join(endpoints)
    r = requests.get(ROOT + endpoint)
    if r.status_code == 200:
        return r.json()
    raise StatusError(r.status_code)

def arbitration_eta(expiry):
    da = datetime.datetime.now()
    de = datetime.datetime.strptime(expiry, FORMAT_DATE)
    duration = de - da
    minutes = (duration.seconds  % 3600) // 60
    return f'expire in **{minutes} mins**'

def sentient_node(code: int) -> str:
    nodes = {
        505: 'Ruse War Field',
        510: 'Gian point',
        550: 'Nsu Grid',
        551: 'Ganalen\'s Grave',
        552: 'Rya',
        553: 'Flexa',
        554: 'H-2 Cloud',
        555: 'R-9 Cloud'
    }
    return nodes[code]

def ws_offi():
    uri = "http://content.warframe.com/dynamic/worldState.php"
    r = requests.get(uri)
    if r.status_code == 200:
        return r.json()
    raise StatusError(r.status_code)

def sentient_time_checker(activation: str) -> bool:
    """If we know next activation event,
    return True else False"""
    now = datetime.datetime.now()
    date_activation = datetime.datetime.strptime(activation, FORMAT_DATE)
    delta_date = activation - now
    return delta_date > 0

def sentient_tlba(activation: str) -> str:
    """Time left before activation"""
    now = datetime.datetime.now()
    date_activation = datetime.datetime.strptime(activation, FORMAT_DATE)
    delta_deta = now - date_activation
    minutes = (duration.seconds  % 3600) // 60
    return f"Sentient ship will be active in **{minutes}**"

def sentient_tlbe(expiry: str) -> str:
    """Time left before expiration"""
    now = datetime.datetime.now()
    date_expiry = datetime.datetime.strptime(expiry, FORMAT_DATE)
    delta_deta = date_expiry - now
    minutes = (duration.seconds  % 3600) // 60
    return f"**{minutes}** mins before sentient ship become inactive"
