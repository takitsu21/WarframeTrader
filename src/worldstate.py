import requests
from src.exceptions import *

root = "https://api.warframestat.us/"

def ws_data(platform: str="pc", *endpoints: list) -> dict:
    endpoint = platform + "/" + '/'.join(endpoints)
    r = requests.get(root + endpoint)
    if r.status_code == 200:
        return r.json()
    raise StatusError(r)
