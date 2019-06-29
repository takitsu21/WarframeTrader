import requests, os

def get_JWT():
    session = requests.Session()
    response = session.get('https://warframe.market/')
    return session.cookies.get_dict()

