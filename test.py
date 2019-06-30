import requests, os
import datetime

def get_JWT():
    session = requests.Session()
    response = session.get('https://warframe.market/')
    return session.cookies.get_dict()

def get_timestamp(file):
    return datetime.datetime.fromtimestamp(os.path.getmtime(file))


print(get_timestamp("graphs/ash_prime_blueprint.png"))