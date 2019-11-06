import requests
from src.exceptions import *
import datetime


root = "https://api.warframestat.us/"

def ws_data(platform: str="pc", *endpoints: list) -> dict:
    endpoint = platform + "/" + '/'.join(endpoints)
    r = requests.get(root + endpoint)
    if r.status_code == 200:
        return r.json()
    raise StatusError(r)

def arbitration_eta(expiry):
    d = datetime.datetime.now()
    d_exp = datetime.datetime.strptime(expiry,"%Y-%m-%dT%H:%M:%S.%fZ")
    d = datetime.datetime(d.year, d.month, d.day, d.hour, d.minute, d.second)
    d_exp = datetime.datetime(d_exp.year, d_exp.month, d_exp.day, d_exp.hour + 1, d_exp.minute, d_exp.second)
    res = datetime.datetime.strptime(str(d_exp - d), '%H:%M:%S')
    return f'expire in **{res.minute} min {res.second} seconds**'

# def vt_eta_activ(activation):
#     d = datetime.datetime.now()
#     d_a = datetime.datetime.strptime(activation,"%Y-%m-%dT%H:%M:%S.%fZ")
#     d = datetime.datetime(d.year, d.month, d.day, d.hour, d.minute, d.second)
#     d_a = datetime.datetime(d_a.year, d_a.month, d_a.day, d_a.hour + 1, d_a.minute, d_a.second)
#     res = datetime.datetime.strptime(str(d_a - d), '%H:%M:%S')
