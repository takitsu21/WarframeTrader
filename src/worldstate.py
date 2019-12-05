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