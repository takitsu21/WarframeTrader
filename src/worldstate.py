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
    d = datetime.datetime.now()
    d_exp = datetime.datetime.strptime(expiry,"%Y-%m-%dT%H:%M:%S.%fZ")
    d = datetime.datetime(d.year, d.month, d.day, d.hour, d.minute, d.second)
    if d_exp.hour != 23:
        d_exp = datetime.datetime(d_exp.year, d_exp.month, d_exp.day, d_exp.hour + 1, d_exp.minute, d_exp.second)
    else:
        d_exp = datetime.datetime(d_exp.year, d_exp.month, d_exp.day + 1, d_exp.hour, d_exp.minute, d_exp.second)
    res = datetime.datetime.strptime(str(d_exp - d), '%H:%M:%S')
    return f'expire in **{res.minute} min {res.second} seconds**'