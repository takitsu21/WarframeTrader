import requests
from src.exceptions import *
import datetime


root = "https://api.warframestat.us/"

def ws_data(platform: str="pc", *endpoints: list) -> dict:
    endpoint = platform + "/" + '/'.join(endpoints)
    r = requests.get(root + endpoint)
    if r.status_code == 200:
        return r.json()
    raise StatusError(r.status_code)

def arbitration_eta(expiry):
    f = "%Y-%m-%dT%H:%M:%S.%fZ"
    da = datetime.datetime.now()
    de = datetime.datetime.strptime(expiry, f)
    duration = de - da
    minutes = (duration.seconds  % 3600) // 60
    return f'expire in **{minutes} mins**'

def sentient_node(code: str) -> str:
    nodes = {
        '505': 'Ruse War Field',
        '510': 'Gian point',
        '550': 'Nsu Grid',
        '551': 'Ganalen\'s Grave',
        '552': 'Rya',
        '553': 'Flexa',
        '554': 'H-2 Cloud',
        '555': 'R-9 Cloud'
    }
    return nodes[code]

def ws_offi():
    uri = "http://content.warframe.com/dynamic/worldState.php"
    r = requests.get(uri)
    if r.status_code == 200:
        return r.json()
    raise StatusError(r.status_code)
